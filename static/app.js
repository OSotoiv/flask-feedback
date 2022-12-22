const $edit_userbtn = $('#edit-user')
const $user_form = $('#user-form')
const $cancel_editbtn = $('#cancel-edit')


$edit_userbtn.click(showHideEditUserForm)
$cancel_editbtn.click(showHideEditUserForm)

function showHideEditUserForm(e) {
    e.preventDefault();
    $edit_userbtn.toggleClass('d-none')
    $user_form.toggleClass('d-none')
}
