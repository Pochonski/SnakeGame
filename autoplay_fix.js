// Función principal para el modo autoplay
function getAutoDirection() {
    // Si ya hay direcciones planificadas, usarlas
    if (plannedDirections.length > 0) {
        return plannedDirections.shift();
    }

    // 1. Buscar un camino directo a la comida
    const pathToFood = findPath(snake, food);
    if (pathToFood && pathToFood.length > 1) {
        const nextPos = pathToFood[1];
        plannedDirections = pathToFood.slice(1).map((pos, i, arr) => {
            if (i === arr.length - 1) return null;
            return {
                x: arr[i + 1].x - pos.x,
                y: arr[i + 1].y - pos.y
            };
        }).filter(Boolean);
        
        // Verificar que el primer movimiento sea seguro
        const nextMove = plannedDirections[0];
        if (nextMove) {
            const newHead = {
                x: snake[0].x + nextMove.x,
                y: snake[0].y + nextMove.y
            };
            if (!isCollision(newHead)) {
                return plannedDirections.shift();
            }
        }
    }

    // 2. Si no hay camino directo, intentar seguir el perímetro
    const perimeterMove = followPerimeter();
    if (perimeterMove) return perimeterMove;

    // 3. Si no hay movimientos seguros en el perímetro, intentar cualquier movimiento seguro
    const safeMove = findSafeMove();
    if (safeMove) return safeMove;

    // 4. Como último recurso, elegir una dirección que no cause colisión
    const possibleMoves = [
        { x: 1, y: 0 },
        { x: -1, y: 0 },
        { x: 0, y: 1 },
        { x: 0, y: -1 }
    ].filter(move => {
        const newX = snake[0].x + move.x;
        const newY = snake[0].y + move.y;
        return !isCollision({ x: newX, y: newY });
    });

    return possibleMoves.length > 0
        ? possibleMoves[Math.floor(Math.random() * possibleMoves.length)]
        : direction; // Mantener dirección actual si no hay movimientos seguros
}

function followPerimeter() {
    // Intentar mantenernos en el perímetro del tablero
    const head = snake[0];
    
    // Si estamos en un borde, seguirlo
    if (head.x === 0 && head.y > 0) return { x: 0, y: -1 }; // Borde izquierdo, subir
    if (head.y === 0 && head.x < tileCount - 1) return { x: 1, y: 0 }; // Borde superior, derecha
    if (head.x === tileCount - 1 && head.y < tileCount - 1) return { x: 0, y: 1 }; // Borde derecho, bajar
    if (head.y === tileCount - 1 && head.x > 0) return { x: -1, y: 0 }; // Borde inferior, izquierda
    
    // Si estamos en una esquina, movernos hacia el centro
    const centerX = Math.floor(tileCount / 2);
    const centerY = Math.floor(tileCount / 2);
    const dx = Math.sign(centerX - head.x);
    const dy = Math.sign(centerY - head.y);
    
    // Intentar primero en la dirección x, luego en y
    if (dx !== 0) {
        const newX = head.x + dx;
        if (!isCollision({ x: newX, y: head.y })) {
            return { x: dx, y: 0 };
        }
    }
    
    if (dy !== 0) {
        const newY = head.y + dy;
        if (!isCollision({ x: head.x, y: newY })) {
            return { x: 0, y: dy };
        }
    }
    
    return null;
}

function findSafeMove() {
    const head = snake[0];
    const possibleMoves = [
        { x: 1, y: 0 },
        { x: -1, y: 0 },
        { x: 0, y: 1 },
        { x: 0, y: -1 }
    ];

    // Ordenar movimientos por distancia a la comida (más cercano primero)
    possibleMoves.sort((a, b) => {
        const distA = Math.abs((head.x + a.x - food.x) ** 2 + (head.y + a.y - food.y) ** 2);
        const distB = Math.abs((head.x + b.x - food.x) ** 2 + (head.y + b.y - food.y) ** 2);
        return distA - distB;
    });

    // Encontrar el primer movimiento seguro
    for (const move of possibleMoves) {
        const newX = head.x + move.x;
        const newY = head.y + move.y;
        
        // Verificar colisión con los bordes
        if (newX < 0 || newY < 0 || newX >= tileCount || newY >= tileCount) {
            continue;
        }
        
        // Verificar si choca con el cuerpo
        let collision = false;
        for (let i = 0; i < snake.length - 1; i++) {
            if (snake[i].x === newX && snake[i].y === newY) {
                collision = true;
                break;
            }
        }
        
        if (!collision) {
            return move;
        }
    }
    
    return null;
}
