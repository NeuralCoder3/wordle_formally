Require Import Lia Vector.
Definition vector := t.
From Hammer Require Import Hammer.
Import VectorNotations.
Require Import List Nat.
Import ListNotations.

Variant feedback := GREEN | ORANGE | BLACK.

(* Variable (f: t feedback 5). *)
(* Check (f [@ (@Fin.of_nat_lt 0 5 _)]). *)


Definition wordle_spec {k} (g w : vector nat k) (f : vector feedback k) (m : vector (option (Fin.t k)) k) := 
    forall i : Fin.t k, 
        ((g[@i]) = (w[@i]) -> (f[@i]) = GREEN /\ (m[@i]) = Some i) /\
        ((f[@i] <> GREEN) -> (exists j, g[@j] = w[@j] /\ m[@j] = Some i) -> f[@i] = ORANGE) /\
        (~(exists j, g[@j] = w[@j]) -> f[@i] = BLACK /\ m[@i] = None).

(* Fixpoint green {k} (g w : vector nat k) : list (Fin.t k) :=
    match g with
    | VectorDef.nil _ => case0 _ [] w
    | VectorDef.cons _ cg k' gr => 
        caseS' w _ (fun cw wr =>
            if cg =? cw then [] else []
        )
    end. *)

(* Definition rect2 {A B} (P:forall {n}, t A n -> t B n -> Type)
  (bas : P [] []) (rect : forall {n v1 v2}, P v1 v2 ->
    forall a b, P (a :: v1) (b :: v2)) :=
  fix rect2_fix {n} (v1 : t A n) : forall v2 : t B n, P v1 v2 :=
  match v1 with
  | [] => fun v2 => case0 _ bas v2
  | @cons _ h1 n' t1 => fun v2 =>
    caseS' v2 (fun v2' => P (h1::t1) v2') (fun h2 t2 => rect (rect2_fix t1 t2) h1 h2)
  end. *)

Goal forall k (g w: vector nat k) f1 f2 m1 m2,
    wordle_spec g w f1 m1 /\ wordle_spec g w f2 m2 -> f1 = f2.
Proof.

    apply (rect2 (fun k g w => forall f1 f2 m1 m2,
            wordle_spec g w f1 m1 /\ wordle_spec g w f2 m2 -> f1 = f2)).
    - intros.
      apply case0.
      pattern f1.
      apply case0.
      congruence.
    - intros.
      apply caseS'.
      intros h2 t2.
      pattern f1.
      apply caseS'.
      intros h1 t1.
      destruct H0 as [H1 H2].

      f_equal.


    (* intros k g w.
    pattern k.
    pattern g.
    pattern w. *)
    (* eapply rect2.
    eapply (rect2 _ _ _). *)
    (* eapply rect2 with (n:=k). *)
    (* intros k g w f1 f2 m1 m2 [H1 H2].
    induction g.
    - revert w f1 f2 m1 m2 H1 H2.
        apply case0. *)
    (* induction g using rectS. *)
    (* intros k g w.
    eapply rect2.
    3: exact g.
    3: exact w.
    -  *)



Definition green {k} (g w : vector nat k) : list (Fin.t k).
    eapply rect2 with (v1 := g).
    3: exact w.
    - exact [].
    - clear k g w.
      intros k g w ys c_g c_w.
      refine(
        if c_g =? c_w then
            (@Fin.F1 k) :: (map Fin.FS ys)
        else (map Fin.FS ys)
      ).
    Defined.

Compute (
    map (fun x => proj1_sig (Fin.to_nat x))
    (green ([0; 1; 2; 3; 4; 5])%vector ([2;1;3;3;4;2])%vector)).

(* Definition orange {k} (g w : vector nat k) (green:list (Fin.t k)) : list (Fin.t k).
    VectorDef.fold_left
        (fun k ) *)



    (* refine (rect2 (fun _ _ => )) *)

    


(*
https://github.com/jdan/wordle.ml/blob/main/lib/evaluator.ml


green = idx list where equal

yellow = 


*)