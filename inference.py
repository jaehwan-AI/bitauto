from fbprophet import Prophet
from neuralprophet import NeuralProphet, set_random_seed
from statsmodels.tsa.arima.model import ARIMA


def predict_arima(x_series, p, d, q, period=120):
    model = ARIMA(x_series, order=(p, d, q))
    fit = model.fit()
    return fit.predict(0, 0+period, typ='levels')


def predict_prophet(x_df, changepoint=0.06, period=120):
    model = Prophet(seasonality_mode='multiplicative',
                    yearly_seasonality=False,
                    weekly_seasonality=False,
                    daily_seasonality=True,
                    changepoint_prior_scale=changepoint)
    model.fit(x_df)
    future_data = model.make_future_dataframe(periods=period, freq='min')
    forecast_data = model.predict(future_data)
    forecast_data[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(5)
    return forecast_data.yhat.values[-period:]


def predict_neuralprophet(x_df, epochs, lr, changepoints, n_forecasts,
                          ar, n_changepoints, trend, period):
    model = NeuralProphet(yearly_seasonality=False,
                          weekly_seasonality=False,
                          daily_seasonality=True,
                          learning_rate=lr, changepoints_range=changepoints,
                          n_forecasts=n_forecasts, ar_sparsity=ar,
                          n_changepoints=n_changepoints, growth='logistic',
                          seasonality_mode='multiplicative',
                          trend_reg=trend)
    model.fit(x_df, plot_live_loss=True, epochs=epochs, freq='m', validate_each_epoch=True, valid_p=0.1)
    model.highlight_nth_step_ahead_of_each_forecast(step_number=model.n_forecasts)
    future_data = model.make_future_dataframe(x_df, periods=period, n_historic_predictions=period)
    forecast_data = model.predict(future_data)
    forecast_data[['ds', 'y', 'yhat1', 'trend']].tail(5)
    return forecast_data.yhat1.values[-period:]
