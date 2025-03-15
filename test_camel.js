const numberPicker = document.getElementById('numberPicker');
const rollButton = document.getElementById('rollButton');
const ResultParagraph = document.getElementById('result');
const diceImages = document.getElementById('diceImages');
const totalParagraph = document.getElementById('total');

function roll(numOfDice) {
    let value;
    let result = [];
    let images = [];
    for (let i = 1; i <= numOfDice; i++) {
        value = Math.floor(Math.random() * 6) + 1;
        result.push(value);
    }
    return result;
}

function imageGenerator(diceArray) {
    let images = [];
    for (let diceValue of diceArray) {
        images.push(`<img src="dice_images/dice${diceValue}.png" alt="dice${diceValue}">`);
    }

    return(images);
}   

rollButton.onclick = function() {
    let diceAmount = Number(numberPicker.value);
    let rollAmount = roll(diceAmount);
    let images = imageGenerator(rollAmount);

    let total = 0;
    for (let number of rollAmount) {
        total += number;
    }

    ResultParagraph.textContent = `You rolled ${diceAmount} dice and got ${rollAmount.join(', ')}`;
    totalParagraph.textContent = `The total is ${total}`;

    diceImages.innerHTML = images.join('');
}