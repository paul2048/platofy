window.onload = () => {
    // Get the list of topics from the database
    $.get('/api/topics/', (topics) => {
        // Configure the topics input form the asking questions form
        $('[name=topics]').tagify({
            whitelist: $.map(topics, (x) => x.name), // Make a list with the names of the topics
            dropdown: {
                classname: 'color-red',
                enabled: 0, // Show the dropdown immediately on focus
                maxItems: 5,
                position: 'text', // Place the dropdown near the typed text
                closeOnSelect: false, // Keep the dropdown open after selecting a suggestion
            }
        });
    });

    // Slides up/down the "ask_form" when the "h1" is clicked
    $('#ask_your_question').click(() => {
        const ask_form = $('#ask_form');

        if (ask_form.css('display') === 'none') {
            ask_form.slideDown();
        } else {
            ask_form.slideUp();
        }
    });

    // When a upvote or downvote button is clicked
    $('.upvote_btn, .downvote_btn').click((e) => {
        const btn = $(e.target).closest('.upvote_btn, .downvote_btn');
        const csrf_token = btn.closest('div[data-csrftoken]').data('csrftoken');
        const user_id = sessionStorage.getItem('user_id');
        const answer_id = btn.closest('[data-id]').data('id');
        const vote_type = btn.hasClass('upvote_btn') ? 'upvote' : 'downvote';
        const data_to_send = {
            csrfmiddlewaretoken: csrf_token,
            user_id: user_id,
            answer_id: answer_id,
            vote_type: vote_type
        }
        btn.removeClass('upvoted');

        $.post('/vote/', data_to_send, (resp) => {
            resp = JSON.parse(resp);
            const btns_cont = btn.parent();

            // Update the new number of points
            btns_cont.find('.points').text(resp.new_points);

            // Color/Uncolor the correct button
            btn.toggleClass('active_vote');
            btn.siblings('div').removeClass('active_vote');

            // Upvote animation
            if (vote_type === 'upvote' && btn.hasClass('active_vote')) {
                btn.addClass('upvoted');
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

        // Store the id of the clicked button (used to display the most recent data after reload)
        localStorage.setItem('recent_profile_btn_id', btn.attr('id'))
    });

    // Get the id of the most recently clicked button in the profile page
    const recent_profile_btn_id = localStorage.getItem('recent_profile_btn_id');
    const recent_profile_btn = $(`#${recent_profile_btn_id}`);

    // If the recently clicked button exists, click it
    if (recent_profile_btn.length) {
        recent_profile_btn.click();
    // Else, click the first button in the button group
    } else {
        $('#profile_btn_group').children().eq(0).click();
    }
};