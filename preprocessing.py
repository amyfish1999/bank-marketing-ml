"""Unfitted Phase 2C preprocessing factories; never loads data or fits on import."""
import warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.utils.validation import check_array, check_is_fitted

CATEGORICAL = ['job', 'marital', 'education', 'default', 'housing', 'loan']
NUMERICAL = ['age', 'previous', 'emp.var.rate', 'cons.price.idx',
             'cons.conf.idx', 'euribor3m', 'nr.employed']
RECENCY = ['recency_days', 'recency_available']
FEATURES = ['age','job','marital','education','default','housing','loan','previous',
            'emp.var.rate','cons.price.idx','cons.conf.idx','euribor3m','nr.employed',
            'recency_available','recency_days']
EXCLUDED = ['duration', 'campaign', 'contact', 'month', 'day_of_week', 'pdays']

class ConditionalRecencyScaler(TransformerMixin, BaseEstimator):
    """Scale observed recency (ddof=0), preserve unavailable zero plus indicator.

    Input columns must be recency_days, recency_available in that order.
    Zero available samples: mean=0, scale=1, warn (no inferred observations).
    One sample/zero variance: observed mean, scale=1, warn.
    Fitting does not use y. Transformation never changes fitted parameters.
    """
    def _checked(self, X):
        if isinstance(X, pd.DataFrame) and list(X.columns) != RECENCY:
            raise ValueError(f'Expected ordered columns {RECENCY}')
        a = check_array(X, dtype=float, ensure_min_samples=0)
        if a.shape[1] != 2:
            raise ValueError('Expected exactly two recency columns')
        if not np.isin(a[:, 1], [0., 1.]).all():
            raise ValueError('recency_available must be binary')
        if (a[:, 0] < 0).any() or ((a[:, 1] == 0) & (a[:, 0] != 0)).any():
            raise ValueError('Expected nonnegative recency and zero unavailable placeholders')
        return a

    def fit(self, X, y=None):
        a = self._checked(X)
        observed = a[a[:, 1] == 1, 0]
        self.n_features_in_ = 2
        self.feature_names_in_ = np.asarray(RECENCY, dtype=object)
        self.n_available_ = len(observed)
        self.mean_ = float(observed.mean()) if self.n_available_ else 0.0
        self.var_ = float(observed.var(ddof=0)) if self.n_available_ else 0.0
        self.scale_ = float(np.sqrt(self.var_)) if self.var_ > 0 else 1.0
        if self.n_available_ < 2 or self.var_ == 0:
            warnings.warn('Insufficient/constant available recency: using unit scale; '
                          'zero available samples also use zero mean.', UserWarning)
        return self

    def transform(self, X):
        check_is_fitted(self, ['mean_', 'scale_', 'n_available_'])
        a = self._checked(X)
        out = np.zeros_like(a, dtype=float)
        available = a[:, 1] == 1
        out[available, 0] = (a[available, 0] - self.mean_) / self.scale_
        out[:, 1] = a[:, 1]
        return out

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, ['mean_'])
        if input_features is not None and list(input_features) != RECENCY:
            raise ValueError(f'Expected input_features={RECENCY}')
        return np.asarray(RECENCY, dtype=object)


def make_preprocessor(model):
    """Return a fresh UNFITTED Pipeline for logistic_regression/decision_tree/random_forest.

    Full one-hot; training-only vocabulary; unseen levels -> all-zero block.
    Dense output is modest for six low-cardinality variables. Nothing is serialized fitted.
    """
    if model not in {'logistic_regression', 'decision_tree', 'random_forest'}:
        raise ValueError('Unknown model configuration')
    lr = model == 'logistic_regression'
    columns = ColumnTransformer([
        ('categorical', OneHotEncoder(drop=None, handle_unknown='ignore',
                                       sparse_output=False, dtype=np.float64), CATEGORICAL),
        ('numerical', StandardScaler() if lr else 'passthrough', NUMERICAL),
        ('recency', ConditionalRecencyScaler() if lr else 'passthrough', RECENCY),
    ], remainder='drop', verbose_feature_names_out=True)
    return Pipeline([('preprocessor', columns)])


def make_cv():
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
