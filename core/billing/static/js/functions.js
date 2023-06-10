$(document).ready(function () {


    /*----------------------------------------------------------------
    Function for search bar
    1. List will be automatically dropped when Searchbar is focused
    2. When Focused is automatically shift focus to last instantly added item
    3. Shortcut to focus Searchbar CTRL + I
    4. Shortcut to Focus Out ESC or ALT
    ----------------------------------------------------------------*/
    // var instantlyAdded = $('#instantly-added');
    const searchBar = $("#search-bar004");
    const searchTarget = $("#search-bar004-target");
    var listItem = $('#search-bar004-target ul li');
    var istab = false;
    var pointer = 0;
    const closeButton = $('#search-close-btn');

    // Search Bar on Focus
    searchBar.on('focus', function () {
        searchTarget.animate({ height: 'show' }, 200);
    });

    closeButton.on('click', function (e) {
        // console.log('hello');
        searchTarget.animate({ height: 'hide' }, 200);
        istab = false;
        searchBar.blur();

    });

    // Search Bar on Focusout
    searchBar.on('blur', function () {
        searchBar.val('');

    });

    // listItem.on('blur', function () {
    //     console.log("Blured");
    //     searchTarget.animate({ height: 'hide' }, 200);
    //     rebaseBackground(pointer);
    //     pointer = 0;
    //     istab = false;
    //     searchBar.blur();
    // });

    /* Keypress Events*/
    $(document).keydown(function (event) {

        if (event.ctrlKey && event.which === 73) { // check for Ctrl+I
            event.preventDefault();
            searchBar.focus();
        }

        if (event.which === 27 || event.altKey) { // check for esc or alt
            event.preventDefault();
            searchTarget.animate({ height: 'hide' }, 200);
            rebaseBackground(pointer);
            pointer = 0;
            istab = false;
            searchBar.blur();
        }

        if (event.which === 9 && searchTarget.is(':visible') && istab == false) { // Check for tab whole Search list is visible3
            event.preventDefault();
            listItem.eq(0).css({ 'background-color': 'gray' });
            istab = true;
        }

        // if (istab) {
        //     let max = $("#search-bar004-target ul li").length;

        //     let half = Math.round(max / 2);

        //     if (event.which === 40 && pointer < max - 1) { /* down arrow */
        //         event.preventDefault();
        //         rebaseBackground();
        //         pointer++;
        //     }

        //     if (event.which === 38) { /* up arrow */
        //         event.preventDefault();
        //         if (pointer > 0) {
        //             rebaseBackground();
        //             pointer--;
        //         }
        //     }
        //     // if (event.which === 39) { /* right arrow */
        //     //     event.preventDefault();
        //     //     let shift = pointer + half;
        //     //     if (shift < max) {
        //     //         rebaseBackground();
        //     //         pointer = shift;
        //     //     }

        //     // }

        //     // if (event.which === 37) { /* left arrow */
        //     //     event.preventDefault();
        //     //     let shift = pointer - half;
        //     //     if (shift >= 0) {
        //     //         rebaseBackground();
        //     //         pointer = shift;
        //     //     }
        //     // }


        //     $('#search-bar004-target ul li').eq(pointer).css({ 'background-color': 'gray' });
        // }

    });


    function rebaseBackground() {
        $('#search-bar004-target ul li').removeAttr('style');
    }
});/* End of  document Ready Function */
