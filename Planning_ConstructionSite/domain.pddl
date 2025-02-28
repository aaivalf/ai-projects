(define (domain construction-site)
(:requirements :strips)
(:predicates (connected ?x ?y)
             (tool-type ?t ?tt)
             (barrier-type ?x ?tt)
             (at ?w ?x)
             (at-worker ?x)
             (location ?p)
             (tool ?t)
             (type ?tt)
             (barrier ?x)
             (holding ?t)
             (open ?x)
             (free ))



(:action clear-barrier
:parameters (?curpos ?barrierpos ?tool ?type)
:precondition (and (location ?curpos) (location ?barrierpos) (tool ?tool) (type ?type)
          (connected ?curpos ?barrierpos) (tool-type ?tool ?type)
                   (barrier-type ?barrierpos ?type) (at-worker ?curpos) 
                   (barrier ?barrierpos) (holding ?tool))
:effect (and  (open ?barrierpos) (not (barrier ?barrierpos))))


(:action move
:parameters (?curpos ?nextpos)
:precondition (and (location ?curpos) (location ?nextpos)
               (at-worker ?curpos) (connected ?curpos ?nextpos) (open ?nextpos))
:effect (and (at-worker ?nextpos) (not (at-worker ?curpos))))

(:action pick-tool
:parameters (?curpos ?tool)
:precondition (and (location ?curpos) (tool ?tool) 
                  (at-worker ?curpos) (at ?tool ?curpos) (free ))
:effect (and (holding ?tool)
   (not (at ?tool ?curpos)) (not (free ))))

(:action switch-tools
:parameters (?curpos ?newtool ?oldtool)
:precondition (and (location ?curpos) (tool ?newtool) (tool ?oldtool)
                  (at-worker ?curpos) (holding ?oldtool) (at ?newtool ?curpos))
:effect (and (holding ?newtool) (at ?oldtool ?curpos)
        (not (holding ?oldtool)) (not (at ?newtool ?curpos))))

(:action put-tool
:parameters (?curpos ?tool)
:precondition (and (location ?curpos) (tool ?tool) 
                  (at-worker ?curpos) (holding ?tool))
:effect (and (free ) (at ?tool ?curpos) (not (holding ?tool)))))
