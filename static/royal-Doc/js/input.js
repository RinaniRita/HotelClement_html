const form = document.getElementById('add-rooms-form');
const roomsDiv = document.getElementById('rooms');
const addRoomButtonTemplate = document.getElementById('add-room-button-template');

let roomGroupIndex = 1;

form.addEventListener('submit', function(event) {
event.preventDefault();

const roomInputs = form.querySelectorAll('.room input');
roomInputs.forEach(function(input) {
    const roomDiv = input.closest('.room');
    const adultsSpan = document.createElement('span');
    adultsSpan.textContent = `Adults: ${input.value}`;
    roomDiv.appendChild(adultsSpan);

    const childrenSpan = document.createElement('span');
    childrenSpan.textContent = `Children: ${input.nextElementSibling.value}`;
    roomDiv.appendChild(childrenSpan);
});

form.reset();
const roomGroups = document.querySelectorAll('#add-rooms-form .room-group');
roomGroups.forEach(function(roomGroup) {
    roomGroup.remove();
});
});

document.addEventListener('click', function(event) {
if (event.target.matches('.add-room-button')) {
    const roomGroupDiv = document.createElement('div');
    roomGroupDiv.classList.add('room-group');

    const addRoomButtonClone = addRoomButtonTemplate.content.cloneNode(true);
    addRoomButtonClone.querySelector('button').addEventListener('click', function() {
    const roomDiv = document.createElement('div');
    roomDiv.classList.add('room');

    const adultsInput = document.createElement('input');
    adultsInput.type = 'number';
    adultsInput.id = `adults-${roomGroupIndex}`;
    adultsInput.name = `adults[]`;
    adultsInput.min = '1';
    adultsInput.required = true;

    const childrenInput = document.createElement('input');
    childrenInput.type = 'number';
    childrenInput.id = `children-${roomGroupIndex}`;
    childrenInput.name = `children[]`;
    childrenInput.min = '0';

    const adultsLabel = document.createElement('label');
    adultsLabel.for = `adults-${roomGroupIndex}`;
    adultsLabel.textContent = 'Number of adults:';

    const childrenLabel = document.createElement('label');
    childrenLabel.for = `children-${roomGroupIndex}`;
    childrenLabel.textContent = 'Number of children:';

    roomDiv.appendChild(adultsLabel);
    roomDiv.appendChild(adultsInput);
    roomDiv.appendChild(childrenLabel);
    roomDiv.appendChild(childrenInput);

    roomGroupDiv.appendChild(roomDiv);

    roomGroupIndex++;
    });

    roomGroupDiv.appendChild(addRoomButtonClone);

    form.insertBefore(roomGroupDiv, form.lastElementChild);
}
});