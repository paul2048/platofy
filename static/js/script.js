window.onload = () => {
    // $('body').fadeIn();

    $('[name=topics]').tagify();
    // $('[name=topics]').data('tagify').addTags('aaa, bbb, ccc');

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