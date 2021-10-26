#-quicklisp
  (let ((quicklisp-init (merge-pathnames "quicklisp/setup.lisp"
                                         (user-homedir-pathname))))
    (when (probe-file quicklisp-init)
      (load quicklisp-init)))

(require "cl-csv")
(use-package :iterate)
; (ql:quickload "cl-csv")
; (ql:quickload "iterate")

(defvar maxScore 290)

;; read a file into a list of lists
(defvar data
  (cl-csv:read-csv #P"consoleGame/records.csv")
)
(defun firstAndThirdElement (it)
  (list (parse-integer (car it)) (parse-integer (caddr it)))
)
(defvar workData
  (map 'list (lambda (it) (firstandthirdelement it)) (cdr data))
)

; More: https://towardsdatascience.com/linear-regression-from-scratch-cd0dee067f72

(defun average (ns)
  (/ (apply '+ ns) (float (length ns)))
)

(defun square (x)
  (* x x)
)

; scoreMean is float
(defvar scoreMean (average (map 'list
                              (lambda (it) (car it))
                              workdata
                         )))
; enemiesMean is flaot
(defvar enemiesMean (average (map 'list
                                (lambda (it) (cadr it))
                                workdata
                           )))

; numerat += (X[i] - x_mean) * (Y[i] - y_mean)
(defvar numerat (apply '+
                       (map 'list (lambda (it)
                                    (* (- (car it) scoremean) (- (cadr it) enemiesmean))
                                  ) workdata
                       )))
; denominator += (X[i] - x_mean) ** 2
(defvar denominat (apply '+
                         (map 'list (lambda (it)
                                      (square (- (cadr it) enemiesmean))
                                    ) workdata
                         )))
(print(format NIL "Denominator: ~F" denominat))
(print (format NIL "Numerator: ~F" numerat))
; b1 = numerat / denominat
(defvar b1 (/ numerat denominat))
(print (format NIL "b1=~F" b1))
; b0 = y_mean - (b1 * x_mean)
(defvar b0 (- scoremean (* b1 enemiesmean)))
(print (format NIL "b0=~F" b0))
(print (format NIL "Score = ~F*enemies + ~F" b1 b0))
(defun getScoreByEnemiesNumber (enemies)
  (+ b0 (* b1 enemies))
)

(defvar rmse (sqrt (/ (apply '+ (map 'list (lambda (it)
                                           (square (- (car it) (getscorebyenemiesnumber (cadr it))))
                                         ) workdata
                              ))
                    (length workdata
                 ))))
(print (format NIL "RMSE = ~F" rmse))
(defvar sumOfSquares (apply '+ (map 'list (lambda (it)
                                          (square (- (car it) scoremean))
                                        ) workdata
                             )))
(defvar sumOfResiduals (apply '+ (map 'list (lambda (it)
                                            (square (- (car it) (getscorebyenemiesnumber (cadr it))))
                                          ) workdata
                               )))
(defvar R2 (- 1 (/ sumofresiduals sumofsquares)))
(print (format NIL "R^2 = ~F" R2))
(defvar newCsvData (map 'list (lambda(it) (list (car it) ( if (= maxScore (cadr it)) "True" "False"  ) (cadr it))) (iter (for i from 1 to 10)
    (collect (list i  (getScoreByEnemiesNumber i))))
))
(print newCsvData)
(terpri)
(defun export-csv (row-data file)
  (with-open-file (stream file :direction :output)
    (cl-csv:write-csv row-data :stream stream)))
(export-csv newCsvData #P"lisp/records.csv")
