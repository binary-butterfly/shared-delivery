export default class UserForm {
    constructor() {
        $('#capabilities').multiselect(window.common.multiselect_options);
        $('#region').multiselect(window.common.multiselect_options);
    }
}