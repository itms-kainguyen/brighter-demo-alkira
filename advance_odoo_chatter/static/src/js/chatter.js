/** @odoo-module **/

import { registerPatch } from "@mail/model/model_core";
import { clear } from "@mail/model/model_field_command";

registerPatch({
  name: "ComposerView",
  recordMethods: {
    /**
     * @override
     */
    onClickSend() {
      this._super.apply(this, arguments);
    },

    async postMessage() {
      const composer = this.composer;
      const postData = this._getMessageData();
      const params = {
        post_data: postData,
        thread_id: composer.thread.id,
        thread_model: composer.thread.model,
      };
      try {
        composer.update({ isPostingMessage: true });
        if (composer.thread.model === "mail.channel") {
          Object.assign(postData, {
            subtype_xmlid: "mail.mt_comment",
          });
        } else {
          Object.assign(postData, {
            subtype_xmlid: composer.isLog ? "mail.mt_note" : "mail.mt_comment",
          });
          if (!composer.isLog) {
            params.context = {
              mail_post_autofollow: this.composer.activeThread.hasWriteAccess,
            };
          }
        }
        if (
          this.threadView &&
          this.threadView.replyingToMessageView &&
          this.threadView.thread !== this.messaging.inbox.thread
        ) {
          postData.parent_id = this.threadView.replyingToMessageView.message.id;
        }
        const { threadView = {} } = this;
        const chatter = this.chatter;
        const { thread: chatterThread } = this.chatter || {};
        const { thread: threadViewThread } = threadView;
        // Keep a reference to messaging: composer could be
        // unmounted while awaiting the prc promise. In this
        // case, this would be undefined.
        const messaging = this.messaging;
        const messageData = await this.messaging.rpc({
          route: `/mail/message/post`,
          params,
        });
        if (!messaging.exists()) {
          return;
        }
        const message = messaging.models["Message"].insert(
          messaging.models["Message"].convertData(messageData)
        );
        if (messaging.hasLinkPreviewFeature && !message.isBodyEmpty) {
          messaging.rpc(
            {
              route: `/mail/link_preview`,
              params: {
                message_id: message.id,
              },
            },
            { shadow: true }
          );
        }
        for (const threadView of message.originThread.threadViews) {
          // Reset auto scroll to be able to see the newly posted message.
          threadView.update({ hasAutoScrollOnMessageReceived: true });
          threadView.addComponentHint("message-posted", { message });
        }
        if (
          chatter &&
          chatter.exists() &&
          chatter.hasParentReloadOnMessagePosted
        ) {
          chatter.reloadParentView();
        }
        if (chatterThread) {
          if (this.exists()) {
            // this.delete();
          }
          if (chatterThread.exists()) {
            // Load new messages to fetch potential new messages from other users (useful due to lack of auto-sync in chatter).
            chatterThread.fetchData([
              "followers",
              "messages",
              "suggestedRecipients",
            ]);
          }
        }
        if (threadViewThread) {
          if (threadViewThread === messaging.inbox.thread) {
            messaging.notify({
              message: sprintf(
                messaging.env._t(`Message posted on "%s"`),
                message.originThread.displayName
              ),
              type: "info",
            });
            if (this.exists()) {
              this.delete();
            }
          }
          if (threadView && threadView.exists()) {
            threadView.update({ replyingToMessageView: clear() });
          }
        }
        if (composer.exists()) {
          composer._reset();
        }
      } finally {
        if (composer.exists()) {
          composer.update({ isPostingMessage: false });
        }
      }
    },
  },
});

registerPatch({
  name: "Chatter",
  recordMethods: {
    closeChatter() {
      this.update({ composerView: clear() });

      $("#close_expand").css({ display: "none" });

      $(".sidebar_chatter_bottom").css({ right: "1rem" });

      $("#expand_chatter").css({ display: "block" });
      $("#collapse_chatter").css({ display: "none" });

      $(".sidebar_chatter_top").removeClass("chatter_icon_top");

      $(".test-ribbon").removeClass("elixir-theme-footer");

      $(".o_ChatterContainer").removeClass("chatter_shadow");

      $(".o_FormRenderer_chatterContainer").removeClass("chatter_form");
      $(".o_Chatter_scrollPanel").css({ display: "none" });
      $(".messages").css({ display: "none" });
      $(".notes").css({ display: "none" });
      $(".activity-container").css({ display: "none" });
    },
    expandChatter() {
      $(".test-ribbon").addClass("elixir-theme-footer");
      $(".sidebar_chatter_bottom").css({ right: "2.2rem" });

      if (!$(".sidebar_chatter_top").hasClass("chatter_icon_top")) {
        $(".sidebar_chatter_top").addClass("chatter_icon_top");
        $("#expand_chatter").css({ display: "none" });
      }
      $("#close_expand").css({ display: "none" });



      $(".o_Chatter_scrollPanel").css({ display: "block" });

      $(".o_ChatterContainer").addClass("chatter_shadow");

      $(".o_FormRenderer_chatterContainer").addClass("chatter_form");
    },

    onclickMsg(ev) {
      this.expandChatter();

      $("#collapse_chatter").css({ display: "block" });
      $(".o_Chatter_scrollPanel").removeClass("chatter_scroll_top");
      $(".notes").css({ display: "none" });
      $(".messages").css({ display: "block" });
      $(".o_Composer").removeClass("o-composer-hide");
      this.showSendMessage();
    },
    onClickNote(ev) {
      this.expandChatter();

      $("#collapse_chatter").css({ display: "block" });

      $(".o_Chatter_scrollPanel").removeClass("chatter_scroll_top");

      $(".messages").css({ display: "none" });

      $(".notes").css({ display: "block" });

      $(".o_Composer").removeClass("o-composer-hide");

      this.showLogNote();

    },

    onClickExpand() {
      this.expandChatter();

      this.update({ composerView: clear() });

      $(".sidebar_chatter_top").removeClass("chatter_icon_top");
      $("#close_expand").css({ display: "block" });

      $(".notes").css({ display: "none" });
      $(".messages").css({ display: "none" });

      $("#collapse_chatter").css({ display: "block" });
      $("#expand_chatter").css({ display: "none" });
      $(".o_Chatter_scrollPanel").addClass("chatter_scroll_top");

    },
    onClickCloseMsg(ev) {
      this.update({ composerView: clear() });
    },
    /**
     * @override
     */
    onClickSendMessage(ev) {
      if ($(".o_Composer").hasClass("o-composer-hide")) {
        $(".o_Composer").removeClass("o-composer-hide");
      } else {
        this._super.apply(this, arguments);
      }
    },
    /**
     * @override
     */
    onClickLogNote() {
      if ($(".o_Composer").hasClass("o-composer-hide")) {
        $(".o_Composer").removeClass("o-composer-hide");
      } else {
        this._super.apply(this, arguments);
      }
    },
    /**
     * @override
     */
    onClickButtonAddAttachments() {
      if ($(".o_Composer").hasClass("o-composer-hide")) {
        $(".o_Composer").removeClass("o-composer-hide");
      } else {
        this._super.apply(this, arguments);
      }
    },
  },
});
