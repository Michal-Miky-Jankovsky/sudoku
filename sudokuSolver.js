// Sudoku solver and game generator
// steps:
// 1. generate a random sudoku board
// 2. solve the board
// 3. remove numbers from the board
// 4. check if the board is still solvable
// 5. if not, go back to step 3
// 6. if yes, return the board

const difficultyMode = {
    easy: 0.5,
    medium: 0.3,
    hard: 0.1
}

function isValidRow(rowArray) {

    const map = new Map([
        [1, false],
        [2, false],
        [3, false],
        [4, false],
        [5, false],
        [6, false],
        [7, false],
        [8, false],
        [9, false]
    ]);

    for (let i = 0; i < rowArray.length; i++) {
        if (rowArray[i] !== undefined) {
            if (map.get(rowArray[i])) {
                return false;
            } else {
                map.set(rowArray[i], true);
            }
        }
    }

    return true;
}

function validBoard(board) {
    for (let pickIndex = 0; pickIndex < 9; pickIndex++) {

        const row = board[pickIndex];

        const col = board.map(row => row[pickIndex]);

        const square = board
            .filter(
                (row, index) =>
                    index >= (Math.floor(row / 3) * 3) &&
                    index < (Math.floor(row / 3) * 3) + 3
            )
            .map(
                row =>
                    row.filter(
                        (col, index) =>
                            index >= (row % 3) * 3 && index < (row % 3) * 3 + 3)
            )
            .reduce(
                (acc, val) =>
                    acc.concat(val), []
            );

        if (!isValidRow(row) || !isValidRow(col) || !isValidRow(square)) {
            return false;
        }
    }
    return true;
}

function nextStep(board, numbersToGenerate, numbersCount) {
    console.log(`numbersCount: ${ numbersCount }`);
    if (numbersCount >= numbersToGenerate) {
        return false;
    }
    const rowIndex = Math.floor(Math.random() * 9);
    const colIndex = Math.floor(Math.random() * 9);
    const number = Math.floor(Math.random() * 9) + 1;

    if (board[rowIndex][colIndex] === undefined) {
        board[rowIndex][colIndex] = number;
        if (validBoard(board)) {
            if (nextStep(board, numbersToGenerate, ++numbersCount))
                return true;
        }
        board[rowIndex][colIndex] = undefined;
        return true;
    }
    return true;
}

function generateBoard() {
    let board = new Array(9);
    for (let i = 0; i < 9; i++) {
        board[i] = new Array(9);
    }

    const numbersToGenerate = 81 * difficultyMode.easy;
    let step = 0;
    let numbersCount = 0;
    while (nextStep(board, numbersToGenerate, numbersCount)) {
        console.log(`counter: ${ step++ }`);
    }
    return board;


    // generate a random board
    // if (validBoard()) {
    //     addRandomly();
    // }
    // return null;

    // return the board

}

const boardToSolve = generateBoard();

console.log(boardToSolve);

