function call_telehealth() {
    document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a").click();

    setTimeout(() => {

        setTimeout(() => {
            document.querySelector("div.MessagingMenuContainer > div > div > div.o_MessagingMenu_dropdownMenuHeader > button:nth-child(3)").click(); 
            setTimeout(() => {
                document.querySelector("div:nth-child(3) > div.o_NotificationListItem_content.o_ChannelPreviewView_content> div.o_NotificationListItem_header.o_ChannelPreviewView_header > span.o_NotificationListItem_name.o_ChannelPreviewView_name").click();

                setTimeout(() => {
                    document.querySelector("div.o_ChatWindowHeader.d-flex.align-items-center.cursor-pointer.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList").click();
                }, 300); 
            }, 300);


        }, 300);





    }, 300);
}