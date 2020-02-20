window.onload = () => {
    // Get the list of topics from the database
    $.get('/api/topics/', (topics) => {
        // Configure the topics input form the asking questions form
        $('[name=topics]').tagify({
            whitelist: $.map(topics, (x) => x.name), // Make a list with the names of the topics
            dropdown: {
                classname: "color-red",
                enabled: 0, // Show the dropdown immediately on focus
                maxItems: 5,
                position: "text", // Place the dropdown near the typed text
                closeOnSelect: false, // Keep the dropdown open after selecting a suggestion
            }
        });
    });

    // When one of the top buttons on the profile page is clicked
    $('#profile_btn_group > button').click((e) => {
        const btn = $(e.target);
        const cont_id = btn.attr('id').replace('_btn', '');
        const cont = $(`#${cont_id}`);

        // Make the clicked button "active"
        btn.parent().children().removeClass('active');
        btn.addClass('active');
        
        // Display the derired container
        cont.parent().children().addClass('d-none');
        cont.removeClass('d-none');
    });
};