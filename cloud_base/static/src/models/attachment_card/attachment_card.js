/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";


registerPatch({
    name: "AttachmentCard",
    recordMethods: {
        /*
        * Re-write to open cloud url if preview is not available
        */
        onClickImage(ev) {
            if ((!this.attachment || !this.attachment.isViewable) && this.attachment.cloudURL) {
                this.onOpenCloudLink(ev);
                return
            }
            else { this._super(ev); }
        },
        /*
        * The method to open the cloud URL if any
        */
        onOpenCloudLink(ev) {
            ev.stopPropagation();
            const cloudLink = document.createElement("a");
            cloudLink.setAttribute("href", this.attachment.cloudURL);
            cloudLink.setAttribute("target", "_blank");
            cloudLink.click();            
        },
    },
});
