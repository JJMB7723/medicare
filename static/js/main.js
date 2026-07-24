document.addEventListener('DOMContentLoaded', function() {
    // 1. Navbar Scroll Effect
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 2. Back to Top Button
    const backToTop = document.querySelector('.back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTop.classList.add('active');
            } else {
                backToTop.classList.remove('active');
            }
        });
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 3. Counter Animation
    const counters = document.querySelectorAll('.counter-value');
    if (counters.length > 0) {
        const runCounters = () => {
            counters.forEach(counter => {
                const target = +counter.getAttribute('data-target');
                const current = +counter.innerText;
                const increment = Math.ceil(target / 100);

                if (current < target) {
                    counter.innerText = Math.min(current + increment, target);
                    setTimeout(runCounters, 20);
                } else {
                    counter.innerText = target;
                }
            });
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    runCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        const statsSection = document.querySelector('.stats-section');
        if (statsSection) {
            observer.observe(statsSection);
        } else {
            // fallback if section not observed
            runCounters();
        }
    }

    // 4. AJAX Doctor Dropdown Loader in Appointment Form
    const deptSelect = document.getElementById('id_department');
    const doctorSelect = document.getElementById('id_doctor');

    if (deptSelect && doctorSelect) {
        // Clear doctor options by default unless editing
        if (!deptSelect.value) {
            doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
        }

        deptSelect.addEventListener('change', function() {
            const url = "/doctors/ajax/load-doctors/";
            const departmentId = this.value;

            if (!departmentId) {
                doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
                return;
            }

            fetch(`${url}?department_id=${departmentId}`)
                .then(response => response.json())
                .then(data => {
                    doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
                    data.forEach(doctor => {
                        const option = document.createElement('option');
                        option.value = doctor.id;
                        option.textContent = `Dr. ${doctor.doctor_name}`;
                        doctorSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error fetching doctors:', error);
                });
        });
    }
});
