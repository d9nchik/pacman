(import [random[randint]]
[copy[copy]])

(setv maze [])
(setv user [0 2])
(setv enemy [3 2])

; Generate our walls
(setv walls [])

(for [x (range 5)](
  do
  (setv points [])
  (points.append (randint 0 4))
  (points.append (randint 0 4))
  (walls.append points)
))

(setv coins [])

; (print walls)

(for [x (range 5)](
  do
  (setv tempArray [])
  (for [y (range 5)](
    do
    (setv point [])
    (point.append x)
    (point.append y)
    (if (and (in point walls) (and (!= point enemy) (!= point user)))
      (tempArray.append 1) (
        do
        (tempArray.append 0)
        (coins.append point)
        ))
  ))
  (maze.append tempArray)
))

(print maze)

(defn getAvailableDirections[point [directionParent None]](
  do
  (setv directions [[0 1] [0 -1] [1 0] [-1 0]])
  (setv availbleDirections [])
  (for [direction directions](
    do
    (setv x (get direction 0))
    (setv y (get direction 1))
    (setv direction [])
    (direction.append (%(+(get point 0) x)5))
    (direction.append (%(+(get point 1) y)5))
    (if (is directionParent None)
    (direction.append (copy direction))
    (direction.append directionParent)
    )
    (if (!= 1 (get maze (get direction 0) (get direction 1)))
    (availbleDirections.append direction))
  ))
  availbleDirections
))

; (print (getAvailableDirections [3 2]))

(defn makeEnemyTurn[enemyPoint userPoint](
  do
  (setv userPointX (get userPoint 0))
  (setv userPointY (get userPoint 1))
  (setv visited [])
  (visited.append enemyPoint)
  (setv nextNodesToVisit (getAvailableDirections enemyPoint))
  (while (!= 0 (len nextNodesToVisit))(
    do
    (setv nodesToVisit nextNodesToVisit)
    (setv nextNodesToVisit [])
    (for [node nodesToVisit](
      do
      (setv node_x (get node 0))
      (setv node_y (get node 1))
      (setv node_without_direction [])
      (node_without_direction.append node_x)
      (node_without_direction.append node_y)
      (if (not (in node_without_direction visited))(
        do
        (visited.append node_without_direction)
        (if (and (= userPointX node_x  (= userPointY node_y)))
        (return (get node 2))
        )
        (+= nextNodesToVisit (getAvailableDirections node (get node 2)))
      ))
    ))
  ))
  (get (getAvailableDirections enemyPoint) 0)
))

(defn pacmanAction[](
  maxTurn 2 user enemy 0
))

(defn maxTurn[deep userPoint enemyPoint score](
  do
  (if (or (= deep 0)(= 0 (len coins)))(
    return score
  ))
  (setv availbleDirections (getAvailableDirections user))
  (setv scores [])
  (for [direction availbleDirections](
    do
    (setv short_direction (cut direction 0 2))
    (setv temp_score score)
    (setv removed_coin None)
    (if (in short_direction coins)(
      do
      (setv temp_score (+ temp_score 1))
      (coins.remove short_direction)
      (setv removed_coin short_direction)
    ))
    ; add coins remove

    (if (= enemyPoint short_direction)(
      scores.append (float "-inf")
    ) (
      do
      (scores.append (+ "branch: " (str(minTurn (- deep 1) short_direction enemyPoint temp_score))))
    ))
    (if (not(is removed_coin None))(
      coins.append short_direction
    ))
  ))
  scores
))

(defn minTurn[deep userPoint enemyPoint score](
  do
  (setv enemy (cut (makeEnemyTurn enemyPoint userPoint) 0 2))
  (if (= enemy userPoint)(
    return (float "-inf")
  )(
    return (maxTurn deep userPoint enemy score)
  ))
))


; (print (makeEnemyTurn enemy user))
(print (pacmanAction ))