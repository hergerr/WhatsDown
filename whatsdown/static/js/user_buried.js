const UIcontroller = (function () {
    const DOMstrings = {
        modalContainer: '.modal-container',
        modalEdit: '#modal-edit',
        modalDelete: '#modal-delete',

        buriedTable: '.table-flex',

        btnEditItem: '.btn-edit-item',
        btnDeleteItem: '.btn-delete-item',
        btnCloseEdit: '.btn-close-edit',
        btnCloseDelete: '.btn-close-delete',

        inputItemEditID: '.input-edit-id',
        inputItemEditFirstName: '.input-edit-first-name',
        inputItemEditLastName: '.input-edit-last-name',
        inputItemEditBirthDate: '.input-edit-birth-date',
        inputItemEditDeathDate: '.input-edit-death-date',
        inputItemCauseOfDeathDate: '.input-edit-cause-of-death',

        inputItemDeleteID: '.input-delete-id'
    };

    return {
        setModalBoxValues: function (event) {
            let item, itemID, itemFirstName, itemLastName, itemBirthDate, itemDeathDate, itemCauseOfDeath;

            item = event.target.parentNode.parentNode;
            itemID = item.id.split('-')[1];
            itemFirstName = item.firstChild.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling;
            itemLastName = itemFirstName.nextSibling.nextSibling;
            itemBirthDate = itemLastName.nextSibling.nextSibling;
            itemDeathDate = itemBirthDate.nextSibling.nextSibling;
            itemCauseOfDeath = itemDeathDate.nextSibling.nextSibling;

            if (event.target.className === "btn btn-edit") {
                document.querySelector(DOMstrings.inputItemEditID).value = itemID;
                document.querySelector(DOMstrings.inputItemEditFirstName).value = itemFirstName.textContent;
                document.querySelector(DOMstrings.inputItemEditLastName).value = itemLastName.textContent;
                document.querySelector(DOMstrings.inputItemEditBirthDate).value = itemBirthDate.textContent;
                document.querySelector(DOMstrings.inputItemEditDeathDate).value = itemDeathDate.textContent;
                document.querySelector(DOMstrings.inputItemCauseOfDeathDate).value = itemCauseOfDeath.textContent;
            }

            if (event.target.className === "btn btn-remove") {
                document.querySelector(DOMstrings.inputItemDeleteID).value = itemID;
            }
        },

        getDOMstrings: function () {
            return DOMstrings;
        }
    };
})();

const controller = (function (UICtrl) {


    function setUpModalButtons() {
        let DOM = UICtrl.getDOMstrings();

        // open editing box
        document.querySelector(DOM.buriedTable).addEventListener('click', event => {
            if(event.target.className === 'btn btn-edit') {
                document.querySelector(DOM.modalEdit).style.display = 'block';
                document.querySelector(DOM.modalContainer).style.display = 'block'
            }

            UICtrl.setModalBoxValues(event);
        });

        // open deleting box
        document.querySelector(DOM.buriedTable).addEventListener('click', event => {
            if(event.target.className === 'btn btn-remove') {
                document.querySelector(DOM.modalDelete).style.display = 'block';
                document.querySelector(DOM.modalContainer).style.display = 'block'
            }

            UICtrl.setModalBoxValues(event);
        });

        // close the editing box
        document.querySelector(DOM.btnEditItem).addEventListener('click', () => {
            if(document.querySelector('.form-edit').valid) {
                document.querySelector(DOM.modalEdit).style.display = 'none';
                document.querySelector(DOM.modalContainer).style.display = 'none'
            }
        });

        document.querySelector(DOM.btnCloseEdit).addEventListener('click', () => {
            document.querySelector(DOM.modalEdit).style.display = 'none';
            document.querySelector(DOM.modalContainer).style.display = 'none'
        });

        // close the deleting box
        document.querySelector(DOM.btnDeleteItem).addEventListener('click', () => {
            document.querySelector(DOM.modalDelete).style.display = 'none';
            document.querySelector(DOM.modalContainer).style.display = 'none'
        });

        document.querySelector(DOM.btnCloseDelete).addEventListener('click', () => {
            document.querySelector(DOM.modalDelete).style.display = 'none';
            document.querySelector(DOM.modalContainer).style.display = 'none'
        });
    }


    return {
        initialize: function() {
            setUpModalButtons();
        },
    };
})(UIcontroller);

controller.initialize();