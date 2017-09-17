(eval-when (:compile-toplevel :execute)
  (ql:quickload '(:usocket :screamer :alexandria :iterate :cl-ppcre :cl-arrows)))

(in-package screamer-user)

(eval-when (:compile-toplevel :execute)
  (use-package '(:usocket :cl-ppcre :cl-arrows)))


(defparameter *issuer-prefixes*
  '(("Visa" (4))
    ("MasterCard" (5 1) (5 2) (5 3) (5 4) (5 5))
    ("American Express" (3 7))
    ("Discover" (6 0 1 1) (6 5))))

(defparameter *card-lengths*
  '(("Visa" . 16)
    ("MasterCard" . 16)
    ("American Express" . 15)
    ("Discover" . 16)))


(defun digit-sum (num)
  (iter:iter
    (iter:while (plusp num))
    (iter:sum (mod num 10))
    (setf num (floor num 10))))

(defun a-random-digit ()
  (a-member-of (alexandria:shuffle (alexandria:iota 10))))

(defun a-random-nonzero-digit ()
  (a-member-of (alexandria:shuffle (alexandria:iota 9 :start 1))))

(defun a-digit-list (length)
  (when (plusp length)
    (list* (a-random-digit) (a-digit-list (1- length)))))

(defun luhn-verify (card)
  (let* ((luhn-sum (loop :for digit :in (reverse card)
                         :for i :from 0
                         :for multiplier := (1+ (mod i 2))
                         :sum (digit-sum (* digit multiplier)))))
    (zerop (mod luhn-sum 10))))

(defun a-card (length &optional prefix)
  (let ((card (-> (append prefix
                          (list (a-random-nonzero-digit))
                          (a-digit-list (- length (length prefix) 1)))
                  (subseq 0 length))))
    (assert! (luhn-verify card))
    card))

(defun assert-suffix (suffix card)
  (mapcar (lambda (a b) (assert! (= a b)))
          (reverse suffix)
          (reverse card)))


(defmacro if-match-bind (vars regex string then else)
  (let ((result (gensym "RESULT")))
    `(let ((,result (nth-value 1 (scan-to-strings ,regex ,string))))
       (if (and ,result (every #'identity ,result))
           (let ,(loop :for var :in vars
                       :for i :from 0
                       :collect `(,var (aref ,result ,i)))
             ,then)
           ,else))))

(defmacro switch-match-bind (string &body cases)
  (when cases
    (if (eq t (caar cases))
        `(progn ,@(cdar cases))
        `(if-match-bind ,(caar cases) ,(cadar cases) ,string
             (progn ,@(cddar cases))
             (switch-match-bind ,string ,@(cdr cases))))))

(cl:defun main ()
  (let* ((s (socket-connect "misc.chal.csaw.io" 8308))
         (ss (socket-stream s)))
    (iter:iter
      (unless (iter:first-iteration-p)
        (write-line (read-line ss)))

      (iter:for line := (read-line ss))
      (write-line line)

      (switch-match-bind line
        ((prefix) "I need a new card that starts with (\\d+)!"
         (-<> (one-value (a-card 16 (map 'list #'digit-char-p prefix)))
              (format nil "~{~A~}" <>)
              (write-line)
              (write-line ss))
         (force-output ss))

        ((suffix) "I need a new card which ends with (\\d+)!"
         (-<> (one-value
                  (let ((card (a-card 16)))
                    (assert-suffix (map 'list #'digit-char-p suffix) card)
                    card))
              (format nil "~{~A~}" <>)
              (write-line)
              (write-line ss))
         (force-output ss))

        ((issuer) "I need a new ([A-Za-z ]+)!"
         (-<> (one-value
                  (a-card (cdr (assoc issuer *card-lengths* :test #'equal))
                          (alexandria:random-elt
                           (cdr (assoc issuer *issuer-prefixes* :test #'equal)))))
              (format nil "~{~A~}" <>)
              (write-line)
              (write-line ss))
         (force-output ss))

        ((candidate) "I need to know if (\\d+) is valid!"
         (-> (if (and (= 16 (length candidate))
                      (luhn-verify (map 'list #'digit-char-p candidate)))
                 1
                 0)
             (write-to-string)
             (write-line)
             (write-line ss))

         (force-output ss)
         (write-line (read-line ss)))

        (() "flag{"
         (return line))

        ;; Else
        (t (print "oops")
           (loop (write-line (read-line ss))))))))
