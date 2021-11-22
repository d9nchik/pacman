(import csv)

(defn getCsv[filename](
  do
    (setv f (open filename))
    (setv records (list (csv.reader f)))
    (f.close)
    records
))

(setv records (cut (getCsv "./consoleGame/records.csv") 1 -1))
; (print (get records 1))
(setv short_data (list(map ( 
  fn [x] (
    do
    (setv array [])
    (array.append (int (get x 2)))
    (array.append (float (get x 3)))  
    (array.append (int (get x 0)))
    array
)) records) ))
; (print short_data)

(defn getMathTimeExpectation [enemiesNumber](
  do
  (setv filteredArray (list(filter (fn [x](= enemiesNumber (get x 0) )) short_data)))
  (setv probability (/ 1 (len filteredArray)))
  (setv mathExpectation (* (sum (lfor x filteredArray (get x 1))) probability))
  mathExpectation
))

(for [x (range 1 11)]
  (print "Enemies: " x "Math Time Expectation: " (getMathTimeExpectation x)))

(defn getDispersion[enemiesNumber](
  do
  (setv filteredArray (list(filter (fn [x](= enemiesNumber (get x 0) )) short_data)))
  (setv probability (/ 1 (len filteredArray)))
  (setv mathExpectation (* (sum (lfor x filteredArray (get x 2))) probability))

  (setv mx_square (* (sum (lfor x filteredArray (** (get x 2) 2))) probability))
  (setv dispersion (- mx_square (** mathExpectation 2)))
  dispersion
))
(print)
(for [x (range 1 11)]
  (print "Enemies: " x "Score Dispersion: " (getDispersion x)))