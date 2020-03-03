// Make sure the code runs after the page was fully loaded
window.onload = () => {
    // Slide down the ask form if the form was opened last lime
    if (JSON.parse(localStorage.getItem('open_ask_form')) === true) {
        $('#ask_form').fadeIn(300);
    }

    // Get the list of topics from the database
    $.get('/api/topics/', (topics) => {
        // Configure the topics input form the asking questions form
        $('[name=topics]').tagify({
            whitelist: $.map(topics, (x) => x.name), // Make a list with the names of the topics
            dropdown: {
                enabled: 0, // Show the dropdown immediately on focus
                maxItems: 5,
                position: 'text', // Place the dropdown near the typed text
                closeOnSelect: false, // Keep the dropdown open after selecting a suggestion
            }
        });
    });

    // Slides up/down the "ask_form" when the "h1" is clicked
    $('#ask_your_question').click(() => {
        $('#ask_form').slideToggle();
        // Negate the value of 'open_ask_form'
        localStorage.setItem('open_ask_form', !JSON.parse(localStorage.getItem('open_ask_form')));
    });

    // When a upvote or downvote button is clicked
    $('.upvote_btn, .downvote_btn').click((e) => {
        const btn = $(e.target).closest('.upvote_btn, .downvote_btn');
        const csrf_token = btn.closest('div[data-csrftoken]').data('csrftoken');
        const answer_id = btn.closest('[data-id]').data('id');
        const vote_type = btn.hasClass('upvote_btn') ? 'upvote' : 'downvote';
        const data_to_send = {
            csrfmiddlewaretoken: csrf_token,
            answer_id: answer_id,
            vote_type: vote_type
        }
        btn.removeClass('upvoted');

        // If the user can't upvote, shows an alert
        const show_alert = (msg) => {
            const card_body = btn.closest('.card-body');
            let alert = card_body.find('.alert');
            // Returns true if the alert should slide down and false if it should fade in 
            const slide = !alert.length;

            alert.remove();
            card_body.append(`
                <div class="alert alert-danger alert-dismissible fade show mt-4" role="alert">
                    <strong>Holy guacamole!</strong> ${msg}
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            `);

            alert = card_body.find('.alert');
            alert.fadeOut(0);

            if (slide) alert.slideDown();
            else alert.fadeIn();
        }

        $.post('/vote/', data_to_send, (resp) => {
            // If a html page (of the login page) was returned
            try {
                resp = JSON.parse(resp);
            } catch (e) {
                show_alert('You must me logged in to vote answers.');
                return;
            }
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
        }).fail((err) => {
            // If a 404 error took place (the answer doesn't exist), append an error message
            if (err.status === 404) {
                show_alert('This answer does\'t exist.It might have been deleted.');
            } else {
                show_alert('Unexpected error.')
            }
        });
    });

    // If the delete button inside the question/answer card is clicked
    $('.delete_qa').click((e) => {
        const btn = $(e.target);
        const card = btn.closest('.qa_card');
        const is_question = !card.find('.points').length;
        const csrf_token = btn.closest('div[data-csrftoken]').data('csrftoken');
        const data_to_send = {
            csrfmiddlewaretoken: csrf_token,
            qa_id: card.data('id'),
            is_question: is_question
        }

        // If the delete confirmation button is clicked
        $('.confr_delete_btn').click(() => {
            $.post('/delete_qa/', data_to_send, (resp) => {
                // If the removal was successful, redirect to the home page
                if (JSON.parse(resp).success) window.location = '/';
            });
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