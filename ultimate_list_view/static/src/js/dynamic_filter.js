/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";
import { Domain } from "@web/core/domain";
import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus } from "@web/core/utils/hooks";
import { DatePicker, DateTimePicker } from "@web/core/datepicker/datepicker";
import { serializeDate, serializeDateTime } from "@web/core/l10n/dates";
import { fuzzyTest } from "@web/core/utils/search";
import { _lt } from "@web/core/l10n/translation";
import { KeepLast } from "@web/core/utils/concurrency";

const { DateTime } = luxon;

let field_date = [DateTime.local()];

const parsers = registry.category("parsers");

const CHAR_FIELDS = [
  "char",
  "html",
  "many2many",
  "many2one",
  "one2many",
  "text",
];
const FIELD_TYPES = {
  boolean: "boolean",
  char: "char",
  date: "date",
  datetime: "datetime",
  float: "number",
  id: "id",
  integer: "number",
  html: "char",
  many2many: "char",
  many2one: "char",
  monetary: "number",
  one2many: "char",
  text: "char",
  selection: "selection",
};

const FIELD_OPERATORS = {
  boolean: [
    { symbol: "=", description: _lt("is Yes"), value: true },
    { symbol: "!=", description: _lt("is No"), value: true },
  ],
  char: [
    { symbol: "ilike", description: _lt("contains") },
    { symbol: "not ilike", description: _lt("doesn't contain") },
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  date: [
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("is after") },
    { symbol: "<", description: _lt("is before") },
    { symbol: ">=", description: _lt("is after or equal to") },
    { symbol: "<=", description: _lt("is before or equal to") },
    { symbol: "between", description: _lt("is between") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  datetime: [
    { symbol: "between", description: _lt("is between") },
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("is after") },
    { symbol: "<", description: _lt("is before") },
    { symbol: ">=", description: _lt("is after or equal to") },
    { symbol: "<=", description: _lt("is before or equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  id: [{ symbol: "=", description: _lt("is") }],
  number: [
    { symbol: "=", description: _lt("is equal to") },
    { symbol: "!=", description: _lt("is not equal to") },
    { symbol: ">", description: _lt("greater than") },
    { symbol: "<", description: _lt("less than") },
    { symbol: ">=", description: _lt("greater than or equal to") },
    { symbol: "<=", description: _lt("less than or equal to") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
  selection: [
    { symbol: "=", description: _lt("is") },
    { symbol: "!=", description: _lt("is not") },
    { symbol: "!=", description: _lt("is set"), value: false },
    { symbol: "=", description: _lt("is not set"), value: false },
  ],
};

const formatters = registry.category("formatters");

function formatField(field, value) {
  if (FIELD_TYPES[field.type] === "char") {
    return value;
  }
  const type = field.type === "id" ? "integer" : field.type;
  const format = formatters.contains(type) ? formatters.get(type) : (v) => v;
  return format(value, { digits: field.digits });
}
let nextItemId = 1;

patch(ListRenderer.prototype, "ultimate_list_view.dynamic_filter", {
  setup() {
    this._super();
    const fields = this.env.searchModel.searchViewFields;
    this.searchItems = this.env.searchModel.getSearchItems(
      (f) => f.type === "field"
    );
    this.items = useState([]);
    this.subItems = {};
    this.keepLast = new KeepLast();
    useBus(this.env.searchModel, "update", this.render);
    this.OPERATORS = FIELD_OPERATORS;
    this.FIELD_TYPES = FIELD_TYPES;
  },

  /**
   * @param {Object} [options={}]
   * @param {number[]} [options.expanded]
   * @param {number} [options.focusedIndex]
   * @param {string} [options.query]
   * @param {Object[]} [options.subItems]
   * @returns {Object[]}
   */
  async searchComputeState(options = {}) {
    const query = "query" in options ? options.query : this.state.query;
    const expanded =
      "expanded" in options ? options.expanded : this.state.expanded;
    const focusedIndex =
      "focusedIndex" in options
        ? options.focusedIndex
        : this.state.focusedIndex;
    const subItems = "subItems" in options ? options.subItems : this.subItems;
    const tasks = [];
    for (const id of expanded) {
      if (!subItems[id]) {
        tasks.push({ id, prom: this.computeSubItems(id, query) });
      }
    }

    const prom = this.keepLast.add(Promise.all(tasks.map((task) => task.prom)));

    if (tasks.length) {
      const taskResults = await prom;
      tasks.forEach((task, index) => {
        subItems[task.id] = taskResults[index];
      });
    }

    this.state.expanded = expanded;
    this.state.query = query;
    this.state.focusedIndex = focusedIndex;
    this.subItems = subItems;
    const trimmedQuery = this.state.query.trim();

    this.items.length = 0;
    if (!trimmedQuery) {
      return;
    }

    for (const searchItem of this.searchItems) {
      const field = this.fields[searchItem.fieldName];
      const type = field.type === "reference" ? "char" : field.type;
      /** @todo do something with respect to localization (rtl) */
      const preposition = this.env._t(
        ["date", "datetime"].includes(type) ? "at" : "for"
      );

      if (["selection", "boolean"].includes(type)) {
        const options = field.selection || [
          [true, this.env._t("Yes")],
          [false, this.env._t("No")],
        ];
        for (const [value, label] of options) {
          if (fuzzyTest(trimmedQuery.toLowerCase(), label.toLowerCase())) {
            this.items.push({
              id: nextItemId++,
              searchItemDescription: searchItem.description,
              preposition,
              searchItemId: searchItem.id,
              label,
              /** @todo check if searchItem.operator is fine (here and elsewhere) */
              operator: searchItem.operator || "=",
              value,
            });
          }
        }
        continue;
      }

      const parser = parsers.contains(type) ? parsers.get(type) : (str) => str;
      let value;
      try {
        switch (type) {
          case "date": {
            value = serializeDate(parser(trimmedQuery));
            break;
          }
          case "datetime": {
            value = serializeDateTime(parser(trimmedQuery));
            break;
          }
          case "many2one": {
            value = trimmedQuery;
            break;
          }
          default: {
            value = parser(trimmedQuery);
          }
        }
      } catch (_e) {
        continue;
      }
      const item = {
        id: nextItemId++,
        searchItemDescription: searchItem.description,
        preposition,
        searchItemId: searchItem.id,
        label: this.state.query,
        operator:
          searchItem.operator || (CHAR_FIELDS.includes(type) ? "ilike" : "="),
        value,
      };
      if (type === "many2one") {
        item.isParent = true;
        item.isExpanded = this.state.expanded.includes(item.searchItemId);
      }

      this.items.push(item);

      if (item.isExpanded) {
        this.items.push(...this.subItems[searchItem.id]);
      }
    }
  },

  /**
   * @param {Object} item
   */
  searchSelectItem(item) {
    if (!item.unselectable) {
      const { searchItemId, label, operator, value } = item;
      this.env.searchModel.addAutoCompletionValues(searchItemId, {
        label,
        operator,
        value,
      });
    }
    this.searchResetState();
  },

  searchResetState() {
    this.searchComputeState({
      expanded: [],
      focusedIndex: 0,
      query: "",
      subItems: [],
    });
  },

  /**
   * @param {InputEvent} ev
   */
  onSearchBarInput(ev) {
    const query = ev.target.value;
    if (query.trim()) {
      this.searchComputeState({
        query,
        expanded: [],
        focusedIndex: 0,
        subItems: [],
      });
    } else if (this.items.length) {
      this.searchResetState();
    }
  },
  /**
   * @param {Object} facet
   */
  removeFacet(facet) {
    this.env.searchModel.deactivateGroup(facet.groupId);
  },

  /**
     * @param {Date} date
     * @param {Name} name
     */
  onDateTimeChanged(date, name) {
    if (date){
      field_date = [date];
        if (this.fields.hasOwnProperty(name)) {
          const field = this.fields[name];
          const genericType = this.FIELD_TYPES[field.type];
          let operator = this.OPERATORS[genericType][0];
          if (genericType === "datetime"){
            operator = this.OPERATORS[genericType][1];
          }
          const descriptionArray = [
            field.string,
            operator.description.toString(),
          ];
          const domainArray = [];
          let domainValue;
          if (["date", "datetime"].includes(genericType)) {
            const serialize = genericType === "date" ? serializeDate : serializeDateTime;
            domainValue = field_date.map(serialize);
            descriptionArray.push(
                `"${field_date
                    .map((val) => formatField(field, val))
                    .join(" " + this.env._t("and") + " ")}"`
            );
          }
          if (operator.symbol === "between") {
            domainArray.push(
              [field.name, ">=", domainValue[0]],
              [field.name, "<=", domainValue[1]]
            );
          } else {
            domainArray.push([field.name, operator.symbol, domainValue[0]]);
          }
          const preFilter = [{
            description: descriptionArray.join(" "),
            domain: new Domain(domainArray).toString(),
            type: 'filter',
          }];
          this.env.searchModel.createNewFilters(preFilter);
        }
    }
  },

  /**
   * @param {KeyboardEvent} ev
   */
  async onSearchBarKeydown(ev) {
    switch (ev.key) {
      case "Enter":

        const preFilters = this.items.map((condition) => {
          const id = ev.target.id;
          if (this.fields.hasOwnProperty(id)) {
            const field = this.fields[id];
            const genericType = this.FIELD_TYPES[field.type];
            const operator = this.OPERATORS[genericType][0];
            const descriptionArray = [
              field.string,
              operator.description.toString(),
            ];
            const domainArray = [];
            let domainValue;
            if ("value" in operator) {
              domainValue = [operator.value];
            } else if (["date", "datetime"].includes(genericType)) {
              const serialize = genericType === "date" ? serializeDate : serializeDateTime;
              condition.value = this.date
              domainValue = condition.value.map(serialize);
              descriptionArray.push(
                  `"${condition.value
                      .map((val) => formatField(field, val))
                      .join(" " + this.env._t("and") + " ")}"`
              );
          } else {
              if (ev.target.value != condition.value) { condition.value = ev.target.value }
              domainValue = [condition.value];
              descriptionArray.push(`"${condition.value}"`);
            }
            if (ev.target.value != domainValue[0]) {
              domainValue[0] = ev.target.value
            }
            if (operator.symbol === "between") {
              domainArray.push(
                [field.name, ">=", domainValue[0]],
                [field.name, "<=", domainValue[1]]
              );
            } else {
              domainArray.push([field.name, operator.symbol, domainValue[0]]);
            }
            const preFilter = {
              description: descriptionArray.join(" "),
              domain: new Domain(domainArray).toString(),
              type: 'filter',
            };
            return preFilter;
          }
        });
        const filter = [preFilters[0]]
        this.env.searchModel.createNewFilters(filter);
        break;
      case "Backspace":
        for (const field_facet of this.env.searchModel.facets) {
          const match = field_facet.values[0].match(/"([^"]+)"/);
          if (match && ev.target.value === match[1]) {
            this.removeFacet(field_facet);
          }
        }
        break;
    }
  },
});

ListRenderer.components = {
  ...ListRenderer.components, // Keep the existing components
  DatePicker,
  DateTimePicker,
};
ListRenderer.template = "web.ListRenderer";