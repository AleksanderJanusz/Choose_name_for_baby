function switch_choises() {
    const switch_buttons = document.querySelector('#over_buttons').children;
    const yes = document.querySelector('#ul-yes');
    const no = document.querySelector('#ul-no');
    const maybe = document.querySelector('#ul-maybe');

    function change_border() {
        for (let button of switch_buttons) {
            button.classList.remove('border-active');
        }
        this.classList.add('border-active');
    }

    function switch_names() {
        yes.classList.add('d-none');
        no.classList.add('d-none');
        maybe.classList.add('d-none');

        if (this.innerText === 'Tak') {
            yes.classList.remove('d-none');
        } else if (this.innerText === 'Nie') {
            no.classList.remove('d-none');
        } else {
            maybe.classList.remove('d-none');
        }
    }

    Array.from(switch_buttons).forEach(element => {
        element.addEventListener('click', function (event) {
            event.preventDefault();
            change_border.call(this);
            switch_names.call(this);

        })
    })
}

document.addEventListener('DOMContentLoaded', function (){
    switch_choises();
})