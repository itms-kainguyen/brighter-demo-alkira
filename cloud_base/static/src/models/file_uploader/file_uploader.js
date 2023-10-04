/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";

registerPatch({
    name: "FileUploader",
    recordMethods: {
        /*
        * Re-write to update folder
        * We do not change _createFormData since in this case it will be needed to fully redevelop the controller
        */
        async _onAttachmentUploaded({ attachmentData, composer, thread }) {
            const _super = this._super.bind(this);
            if (thread && thread.cloudsFolderId && !composer) {
                // When we are from composer, message will be allocated to the folder in postprocess
                await this.messaging.rpc({
                    model: "ir.attachment",
                    method: "write",
                    args: [[attachmentData.id], {"clouds_folder_id": thread.cloudsFolderId}]
                });
                await thread.fetchFolderAttachments();
            };
            return _super(...arguments);
        },
    },
});
