"""Synthetic unit tests only: no held-out data or fitted production artifacts."""
import unittest
import warnings
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from preprocessing import ConditionalRecencyScaler, RECENCY, make_preprocessor

class ConditionalRecencyTests(unittest.TestCase):
    def frame(self, rows):
        return pd.DataFrame(rows, columns=RECENCY)

    def test_observed_only_and_no_refit(self):
        train = self.frame([[0,0]]*100 + [[0,1],[2,1],[4,1]])
        s = ConditionalRecencyScaler().fit(train)
        self.assertEqual(s.n_available_, 3)
        self.assertEqual(s.mean_, 2)
        self.assertAlmostEqual(s.var_, 8/3)
        np.testing.assert_allclose(s.scale_, np.std([0,2,4], ddof=0))
        state = (s.mean_,s.scale_,s.var_,s.n_available_)
        out = s.transform(self.frame([[0,0],[0,1],[1000,1]]))
        np.testing.assert_array_equal(out[0], [0,0])
        self.assertEqual(out[1,1], 1)
        self.assertNotEqual(out[1,0], out[0,0])
        self.assertEqual((s.mean_,s.scale_,s.var_,s.n_available_), state)
        # Adding any number of unavailable placeholders cannot affect fitted statistics.
        t = clone(s).fit(self.frame([[0,1],[2,1],[4,1]]))
        self.assertEqual((t.mean_,t.var_,t.scale_), (s.mean_,s.var_,s.scale_))
        np.testing.assert_array_equal(s.get_feature_names_out(), RECENCY)

    def test_safe_fallbacks(self):
        for rows,mean,n in [([[0,0],[0,0]],0,0), ([[0,0],[4,1]],4,1),
                            ([[3,1],[3,1]],3,2), ([[0,1],[0,1]],0,2)]:
            with self.assertWarns(UserWarning):
                s=ConditionalRecencyScaler().fit(self.frame(rows))
            self.assertEqual(s.mean_,mean); self.assertEqual(s.scale_,1)
            self.assertEqual(s.n_available_,n)
            out=s.transform(self.frame([[0,0],[0,1],[4,1]]))
            self.assertTrue(np.isfinite(out).all())
            # Even when both transformed day values are zero, indicator distinguishes them.
            self.assertEqual(out[0,1],0); self.assertEqual(out[1,1],1)

    def test_invalid_input_and_unfitted(self):
        with self.assertRaises(NotFittedError):
            ConditionalRecencyScaler().transform(self.frame([[0,0]]))
        for rows in [[[1,0]], [[-1,1]], [[0,2]], [[np.nan,1]], [[np.inf,1]]]:
            with self.assertRaises(ValueError):
                ConditionalRecencyScaler().fit(self.frame(rows))
        with self.assertRaises(ValueError):
            ConditionalRecencyScaler().fit(pd.DataFrame({'wrong':[0], 'names':[1]}))

    def test_factory_is_unfitted_and_cloneable(self):
        for model in ['logistic_regression','decision_tree','random_forest']:
            p=make_preprocessor(model)
            clone(p)
            self.assertFalse(hasattr(p.named_steps['preprocessor'],'transformers_'))
        with self.assertRaises(ValueError):make_preprocessor('unsupported')

if __name__=='__main__':
    unittest.main()
