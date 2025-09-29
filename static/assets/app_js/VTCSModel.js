AppVTCSModel = function () {

    let me = this;
    me.appConstructor = function () {

    };

    me.EditVTCSTripData_ShowModel = function () {
        // alert("fff");

        // $("#effect-modal-header").empty();

        $("#effect-modal-header").empty();
        $("#effect-modal-header").append('<h6 class="modal-title text-capitalize" id="set_title"></h6>' +
            '<button aria-label="Close" class="btn-close" data-bs-dismiss="modal" type="button">' +
            '<span aria-hidden="true">×</span></button>');

        $("#effect-modal-body").html("");
        var container_body = $("#effect-modal-body");
        container_body.append('<div class="mb-3">' +
            "<input type='hidden' id='action_type_l2' name='action_type_l2' value='' autocomplete='off'>" +
            '</div>' +
            '</div>');

        $("#effect-modal-footer").html("");
        var container_footer = $("#effect-modal-footer");
        container_footer.append('<button onclick="COAModelJS.AddSubParent_COA();" class="btn btn-sm w-50 btn-success" type="button">Save Sub Parent</button>' +
            '<button class="btn btn-sm w-25 btn-danger" data-bs-dismiss="modal" type="button">Close</button>');

        $('#effectModal').modal('show');

    }

}