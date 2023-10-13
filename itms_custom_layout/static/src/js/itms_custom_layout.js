function call_telehealth() {
    document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a").click();

    setTimeout(() => {

        document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > div > div.o_NotificationList.d-flex.flex-column.overflow-auto.o_MessagingMenu_notificationList > div:nth-child(13) > div.o_NotificationListItem_content.o_ChannelPreviewView_content.d-flex.flex-column.flex-grow-1.align-self-start.m-2 > div.o_NotificationListItem_header.o_ChannelPreviewView_header.d-flex.align-items-baseline > span.o_NotificationListItem_name.o_ChannelPreviewView_name.text-truncate.fw-bold.o-muted.text-600").click();

        setTimeout(() => {
            document.querySelector("div.o_ChatWindowHeader.d-flex.align-items-center.cursor-pointer.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList").click()
        }, 300);




    }, 300);
}