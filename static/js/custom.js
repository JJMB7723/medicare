// Custom JavaScript for MediCare H.M.S.

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Back to Top Button
    const mybutton = document.getElementById("btn-back-to-top");
    if (mybutton) {
        window.onscroll = function () {
            scrollFunction();
        };

        function scrollFunction() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                mybutton.style.display = "flex";
            } else {
                mybutton.style.display = "none";
            }
        }

        mybutton.addEventListener("click", function() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    // 2. Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // 3. Stats Counter Animation
    const counters = document.querySelectorAll('.counter-val');
    if (counters.length > 0) {
        const speed = 200; // lower is faster
        
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 1);
                } else {
                    counter.innerText = target;
                }
            };
            updateCount();
        });
    }

    // 4. Client-side Cascading Dropdown for Department -> Doctor
    const deptSelect = document.getElementById('id_department');
    const doctorSelect = document.getElementById('id_doctor');

    if (deptSelect && doctorSelect) {
        const originalDoctorOptions = Array.from(doctorSelect.options);

        deptSelect.addEventListener('change', function() {
            const selectedDeptId = deptSelect.value;
            
            // Clear current doctor choices
            doctorSelect.innerHTML = '';

            // Filter and append options
            originalDoctorOptions.forEach(option => {
                const optDeptId = option.getAttribute('data-department');
                // Always append the placeholder option (empty value)
                if (option.value === "" || optDeptId === selectedDeptId) {
                    doctorSelect.appendChild(option.cloneNode(true));
                }
            });
        });
    }
});
