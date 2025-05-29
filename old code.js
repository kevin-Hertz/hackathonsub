const cube = document.querySelector('.cube');
let mouseX = 0;
let mouseY = 0;
const rotationValue = 360

const handlemouseMove = (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
    rotax = -(mouseY / window.innerHeight - 0.5) * rotationValue;
    rotay = (mouseX / window.innerWidth - 0.5) * rotationValue;
    cube.style.transform = `rotateX(${rotax}deg) rotateY(${rotay}deg)`;
};

window.addEventListener('mousemove', handlemouseMove);