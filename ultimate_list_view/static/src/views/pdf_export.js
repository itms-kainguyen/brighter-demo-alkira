/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";

import { patch } from "@web/core/utils/patch";


var ajax = require('web.ajax');
ListController.prototype.actionDef = async function(){
    var self=this;

    var listRecords = document.getElementsByClassName("o_list_table");
    var rows = listRecords[0].getElementsByTagName("tr");
    var records = [];
    // Get the field names from the table header
    var headerCells = rows[0].getElementsByTagName("th");
    var fieldNames = [];

    for (var k = 0; k < headerCells.length; k++) {
      fieldNames.push(headerCells[k].innerText);
    }
    records.push(fieldNames.join("\t")); // Include field names as the first row

    const fields = this.props.archInfo.columns
        .filter((col) => col.type === "field")
        .map((col) => this.props.fields[col.name])

    const exportedFields = fields.map((field) => ({
        name: field.name,
        label: field.label || field.string,
    }));
    const resIds = await this.getSelectedResIds();
    const execute = () => {
        const matchingFields = [];
        fieldNames.forEach((fieldName) => {
            // Check if the field name is in the listFields
            const matchingField = exportedFields.find((field) => field.label === fieldName);
        
            if (matchingField) {
                matchingFields.push(matchingField);
            } 
        });

        var length_field = Array.from(Array(matchingFields.length).keys());
        ajax.jsonRpc('/get_data','call',{
        'model':this.model.root.resModel,
        'res_ids':resIds.length > 0 && resIds,
        'fields':matchingFields,
        'grouped_by':this.model.root.groupBy,
        'context': this.props.context,
        'domain':this.model.root.domain,
        'context':this.props.context,
        }).then( function (data){
            if (self.model.root.groupBy[0]){
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name':'ultimate_list_view.export_in_pdf_group_by',
                    'data':{'length':length_field,'group_len':[0,1,2,3],'record':data,}
                };
            }
            else{
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name':'ultimate_list_view.export_in_pdf',
                    'data':{'length':length_field,'record':data}
                };
                return self.model.action.doAction(action);
            }
        });
    };

    execute();
}

patch(ListController.prototype, "ultimate_list_view.list_controller", {
    setup() {
      this._super();
    },
    async exportOnDirectExportDataXlsx(){
    if (this.defaultExportList) 
    {
        await this.downloadExport(this.defaultExportList, false, "xlsx");
    } 
    else{
    const fields = this.props.archInfo.columns
    .filter((col) => col.type === "field")
    .map((col) => this.props.fields[col.name])
    .filter((field) => field.exportable !== false);
    console.log("fields :", fields);
    await this.downloadExport(fields, false, "xlsx");
    }
    },

    async exportOnDirectExportDataCsv(){
    if (this.defaultExportList) {
    await this.downloadExport(this.defaultExportList, false, "csv");
    }
    else{
    const fields = this.props.archInfo.columns
    .filter((col) => col.type === "field")
    .map((col) => this.props.fields[col.name])
    .filter((field) => field.exportable !== false);
    console.log("fields :", fields);
    await this.downloadExport(fields, false, "csv");
    }
    }
})



