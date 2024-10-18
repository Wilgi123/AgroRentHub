document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav ul li a');

    navLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.color = '#ffeb3b';
        });

        link.addEventListener('mouseout', () => {
            link.style.color = 'white';
        });
    });
});
/*document.addEventListener('DOMContentLoaded', function() {
    const contentBox = document.getElementById('content-box');
    const links = document.querySelectorAll('.sidenav a');

    const content = {
        about: `
            <h2>About Us</h2>
            <p>We are committed to providing the best agricultural rental services. Our mission is to support farmers by offering high-quality rental equipment.</p>
            <p>Our team is dedicated to helping you achieve your farming goals with our reliable and affordable rental solutions.</p>
        `,
        services: `
            <h2>Our Services</h2>
            <ul>
                <li>Tractor Rentals</li>
                <li>Harvesting Equipment</li>
                <li>Plowing Tools</li>
                <li>Seeding Machines</li>
                <li>Irrigation Systems</li>
            </ul>
            <p>We offer a wide range of services to meet your agricultural needs. Contact us to learn more about our services and how we can help you.</p>
        `,
        clients: `
            <h2>Our Clients</h2>
            <p>We are proud to have served a diverse group of clients, including small family farms and large agricultural enterprises.</p>
            <p>Our clients value our commitment to quality and our reliable service. Join our growing list of satisfied customers today.</p>
        `,
        contact: `
            <h2>Contact Us</h2>
            <p>We would love to hear from you! Reach out to us with any questions or to learn more about our services.</p>
            <p>Email: info@agrirent.com</p>
            <p>Phone: (123) 456-7890</p>
            <p>Address: 1234 Farm Lane, Agriculture City, AG 56789</p>
        `
    };

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = e.target.getAttribute('data-content');
            contentBox.innerHTML = content[section];
        });
    });
});*/
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('workers-yes').addEventListener('click', function () {
        document.getElementById('workers-question').style.display = 'none';
        document.getElementById('workers-container').style.display = 'block';
    });

    document.getElementById('workers-no').addEventListener('click', function () {
        document.getElementById('workers-question').style.display = 'none';
    });

    document.getElementById('toggle-workers').addEventListener('click', function () {
        var workersForm = document.getElementById('workers-form');
        if (workersForm.style.display === 'none' || workersForm.style.display === '') {
            workersForm.style.display = 'block';
        } else {
            workersForm.style.display = 'none';
        }
    });

    document.getElementById('cancel-workers').addEventListener('click', function () {
        document.getElementById('workers-form').style.display = 'none';
    });

    document.getElementById('workers-details-form').addEventListener('submit', function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                document.getElementById('workers-summary').style.display = 'block';
                document.getElementById('workers-summary-content').innerHTML = `
                    <p>Number of Workers: ${data.num_workers}</p>
                    <p>Worker Type: ${data.work_type}</p>
                    <p>Start Date: ${data.start_date}</p>
                    <p>End Date: ${data.end_date}</p>
                `;
                document.getElementById('total-workers-cost').textContent = data.total_workers_cost;
                document.getElementById('workers-container').style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
