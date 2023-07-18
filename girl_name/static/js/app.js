function switch_choises(switch_buttons, yes, no, maybe) {

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

document.addEventListener('DOMContentLoaded', function () {
    const switch_buttons = document.querySelector('#over_buttons').children;
    const yes = document.querySelector('#ul-yes');
    const no = document.querySelector('#ul-no');
    const maybe = document.querySelector('#ul-maybe');
    const names = document.querySelectorAll('.wide-div a');

    switch_choises(switch_buttons, yes, no, maybe);

    names.forEach(name => {
        name.addEventListener('dragstart', function (event) {
            selected_name = event.target;
        })

        Array.from(switch_buttons).forEach(button => {
            button.addEventListener('dragover', function (event) {
                event.preventDefault();
            })
            button.addEventListener('drop', function (event) {
                event.preventDefault();
                event.stopImmediatePropagation();

                if (this.innerText === 'Tak') {
                    let li = document.createElement('li');
                    console.log(selected_name)
                    li.appendChild(selected_name);
                    yes.appendChild(li);
                } else if (this.innerText === 'Nie') {
                    let li = document.createElement('li');
                    li.appendChild(selected_name);
                    no.appendChild(li);
                } else {
                    let li = document.createElement('li');
                    li.appendChild(selected_name);
                    maybe.appendChild(li);
                }
            })
        })

    })
})