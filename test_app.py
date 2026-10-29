"""Smoke tests: run the app headlessly with every dataset/model/option and check there are no errors.
Run: python test_app.py"""
import itertools
import pandas as pd
from streamlit.testing.v1 import AppTest

import validation_lib as vl


def sl(at, label):
    return next(s for s in at.slider if s.label == label)


def rad(at, label):
    return next(s for s in at.radio if s.label == label)


def run_all():
    n = 0
    for ds, model, strat, metric in itertools.product(
        vl.SAMPLE_DATASETS, vl.MODELS, [True, False], list(vl.METRICS)
    ):
        if metric != "Accuracy" and model != "Logistic Regression":
            continue
        at = AppTest.from_file("app.py", default_timeout=120).run()
        at.selectbox[0].set_value(ds)
        at.selectbox[1].set_value(model)
        at.selectbox[2].set_value(metric)
        at.toggle[0].set_value(strat)
        sl(at,"k (number of folds)").set_value(7)
        at = at.run()
        assert not at.exception, (ds, model, strat, metric, at.exception)
        n += 1
    # leak switch, reshuffle, k range
    at = AppTest.from_file("app.py", default_timeout=120).run()
    rad(at,"Where does scaling happen?").set_value("Before the split (leaks)").run()
    assert not at.exception
    for k in (3, 10):
        sl(at,"k (number of folds)").set_value(k).run()
        assert not at.exception, at.exception
    at.button[0].click().run()
    assert not at.exception
    print(f"OK: {n} combinations + leak switch + k + reshuffle")


def test_lib():
    d = vl.prepare_csv(pd.read_csv("sample_data/customer_churn_sample.csv"), "churned")
    assert d.n_rows == 600 and len(d.class_names) == 2
    try:
        vl.prepare_csv(pd.DataFrame({"a": range(50), "t": [i * 0.37 for i in range(50)]}), "t")
        raise SystemExit("expected ValueError")
    except ValueError:
        pass
    assert vl.advise(60, .5, 30).method == "LOOCV"
    assert vl.advise(500, .5, 250).method == "K-fold"
    assert vl.advise(1000, .05, 50).method == "Stratified K-fold"
    assert vl.advise(500_000, .5, 1).method == "Hold-out split"
    for n, m in [(60, .5), (500, .5), (1000, .05), (500_000, .5), (2_000_000, .02)]:
        compile(vl.advise(n, m, max(2, int(n * m))).code, "snippet", "exec")
    print("OK: lib tests")


if __name__ == "__main__":
    test_lib()
    run_all()
