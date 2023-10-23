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

function call_telehealth_dashboard() {
    setVisible('#loading', true);


    // click on the top bar message
    if (!Object.is(document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a"), null)) {
        document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a").click();
    }


    setTimeout(() => {


        // click on the tab channels
        if (!Object.is(document.querySelector("div.MessagingMenuContainer > div > div > div.o_MessagingMenu_dropdownMenuHeader > button:nth-child(3)"), null)) {
            document.querySelector("div.MessagingMenuContainer > div > div > div.o_MessagingMenu_dropdownMenuHeader > button:nth-child(3)").click();
        }

        // make smooth


        setTimeout(() => {
            // click on the prescriber button

            if (!Object.is(document.querySelector("div:nth-child(3) > div.o_NotificationListItem_content.o_ChannelPreviewView_content> div.o_NotificationListItem_header.o_ChannelPreviewView_header > span.o_NotificationListItem_name.o_ChannelPreviewView_name"), null)) {
                document.querySelector("div:nth-child(3) > div.o_NotificationListItem_content.o_ChannelPreviewView_content> div.o_NotificationListItem_header.o_ChannelPreviewView_header > span.o_NotificationListItem_name.o_ChannelPreviewView_name").click();
            }


            setTimeout(() => {
                setVisible('#loading', false);
                if (!Object.is(document.querySelector("div.o_ChatWindowHeader.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList"), null)) {
                    document.querySelector("div.o_ChatWindowHeader.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList").click();

                }

            }, 300);
        }, 300);


    }, 300);
}


function close_telehealth() {
    setTimeout(() => {
        if (!Object.is(document.querySelector("div.o_ChatWindowHeader.d-flex.align-items-center.cursor-pointer.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandClose"), null)) {

            document.querySelector("div.o_ChatWindowHeader.d-flex.align-items-center.cursor-pointer.o_ChatWindow_header > div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea> div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandClose").click();
        }


        setVisible('#loading', false);


    }, 1500);
}


function clone_telehealth_dashboard() {
    setTimeout(() => {
        $('.o_ChannelMemberList').appendTo("#dashboard_prescribers");

    }, 1300);
}


function call_close_chatbox() {

    $('.o_ChatWindowHeader_command.o_ChatWindowHeader_commandClose').on('click', function () {
        var style = document.createElement('style');
        style.innerHTML = `
                                        .o_ChatWindow {
                                          opacity: 0 !important;
                                          z-index: -1 !important;
                                        }
                                        `;
        document.head.appendChild(style);
        setVisible('#loading', false);

    });
}


function setVisible(selector, visible) {
    if (visible) {
        $(selector).css("display", "block");
    } else {
        $(selector).css("display", "none");
    }
}


/** mobile version
 *
 *
 *
 *
 *
 *
 */


function call_telehealth_dashboard_mobile() {
    setVisible('#loading', true);



    setTimeout(() => {
        // click on the top bar message
        if (!Object.is(document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a"), null)) {
            document.querySelector("body > header > nav > div.o_menu_systray.d-flex.flex-shrink-0.ms-auto > div.MessagingMenuContainer > div > a").click();

        }

        setTimeout(() => {


            // click on the tab channels
            if (!Object.is(document.querySelector("div.o_menu_systray> div.MessagingMenuContainer > div > div > div.o_MobileMessagingNavbar.o_MessagingMenu_mobileNavbar > div.o_MobileMessagingNavbar_tab:nth-child(3)")
            )) {
                document.querySelector("div.o_menu_systray> div.MessagingMenuContainer > div > div > div.o_MobileMessagingNavbar.o_MessagingMenu_mobileNavbar > div.o_MobileMessagingNavbar_tab:nth-child(3)").click();


            }

            // make smooth


            setTimeout(() => {
                // click on the prescriber button

                if (!Object.is(document.querySelector("div:nth-child(3) > div.o_NotificationListItem_content.o_ChannelPreviewView_content> div.o_NotificationListItem_header.o_ChannelPreviewView_header > span.o_NotificationListItem_name.o_ChannelPreviewView_name"), null)) {

                    document.querySelector("div:nth-child(3) > div.o_NotificationListItem_content.o_ChannelPreviewView_content> div.o_NotificationListItem_header.o_ChannelPreviewView_header > span.o_NotificationListItem_name.o_ChannelPreviewView_name").click();
                }


                setTimeout(() => {
                    setVisible('#loading', false);
                    if (!Object.is(document.querySelector("div.o_ChatWindowManager > div > div.o_ChatWindowHeader.o_ChatWindow_header> div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea > div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList"))) {
                        document.querySelector("div.o_ChatWindowManager > div > div.o_ChatWindowHeader.o_ChatWindow_header> div.o_ChatWindowHeader_item.o_ChatWindowHeader_rightArea > div.o_ChatWindowHeader_command.o_ChatWindowHeader_commandShowMemberList").click();
                    }

                }, 300);
            }, 300);


        }, 300);

    }, 300);


}