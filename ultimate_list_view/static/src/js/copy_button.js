odoo.define('ultimate_list_view.copy_button', function (require) {
  "use strict";

  var rpc = require('web.rpc');
  var core = require('web.core');
  var _t = core._t;

  function onCopyClick() {
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

    for (var i = 1; i < rows.length; i++) { // Start from index 1 to skip the header row
      var cells = rows[i].getElementsByTagName("td");
      var record = [];

      for (var j = 0; j < cells.length; j++) {
        record.push(cells[j].innerText);
      }

      records.push(record.join("\t")); // Separate values with a tab ("\t")
    }

    var copiedData = records.join("\n"); // Separate rows with a new line ("\n")

    // Copy the result to the clipboard
    var tempInput = document.createElement('textarea');
    tempInput.value = copiedData;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    // Show a notification with the number of records copied
    var recordCount = records.length - 1; // Subtract 1 to exclude the header row
    var message = _t("Copied ") + recordCount + " " + _t("record(s)") + " " + _t("to the clipboard");
    alert(message);

    console.log('Success');
    console.log(copiedData);
  }

  window.onCopyClick = onCopyClick;
});
