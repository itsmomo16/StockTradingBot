

//@version=5
strategy("𝐉𝐔𝐈𝐂𝐘 𝐓𝐑𝐄𝐍𝐃", overlay=true, initial_capital=2000, default_qty_type=strategy.percent_of_equity, default_qty_value=30, commission_value=0.075)

//Tool Tips/////////////////////////////////////////////////////////////////////
tttradetrend        = "Only \"BUY\" when \"MA 3\" is trending up. If enabled, \"BUY\" orders will not be executed when \"MA 3\" is going down.\nThis can help reduce drawdown and increase profitability, but usually decreases net profit significantly.\nMore trades will end in profit, but you will miss out on many profitable opportunities."
ttsellaftertrend    = "If you are only trading with the trend, there may be a position which remains open after that trend has ended./nThis option will force that final trade to close to limit the loss and get the strategy back into action on the next uptrend."
ttsellout           = "If \"Sell After Trend Reverses\" is enabled, the position will be sold this number of bars/candles after the trend has reversed down."
ttsellinprofit      = "Only exit trades when the position is in profit or when the stop loss is triggered.\nIf enabled, and \"Use Stop Loss\" is disabled, the trade may wait a long time before the price comes up into profit."
ttminimumprofit     = "If \"Only Sell in Profit\" is enabled, this determines how far in profit the position must be for a sell signal to be valid."
ttusetakeprofit     = "Use the take profit percentage to prematurely end trades in profit. This may decrease the number of losing trades."
tttakeprofitpercent = "Set how far the price should climb before the trade is closed at market price in profit.\n It may be more profitable to prematurely close a trade because a sell signal might not be triggered depending on price action."
ttusestoploss       = "Use the stop loss percentage to limit the loss endured when the price dumps.\nIf disabled, and \"Only Sell in Profit\" is disabled, the price could dump and then receive a sell signal at a losing position."
ttstoplosspercent   = "Set how far the price should drop before the trade is closed at market price in a loss.\nIt may be more profitable long term to endure larger losses, less often."
ttexpireoption      = "This feature forces a trade to close at market price after the chosen number of candles/bars have passed.\n To clarify, if no sell/stop/take signal was received then the trade will close in a profit or loss after the chosen number of candles/bars have passed."
ttexpiretime        = "Choose how many bars/candles should pass before the trade expires and closes at market price.\nIn a downtrend on MA 3, this value is halved."
ttma1               = "\"MA 1\" should follow the price closely while reducing as much noise as possible.\n\"BUY\" and \"SELL\" signals are based on \"MA 1\" and \"MA 2\" crosses.\nAdjust them to flow with your asset and timeframe as profitably as possible."
ttma2               = "\"MA 2\" should not make contact with \"MA 1\" until the direction of price has started reversing.\nTry to keep the lines seperated, only crossing on pivot highs and pivot lows."
ttma3               = "If \"Only Trade with Trend\" is enabled, \"MA 3\" will restrict trades to it's direction.\n\"BUY\" trades will only be executed in an uptrend."
ttusestochrsi       = "Decide whether to consider the position of the Stochastic RSI. If enabled, a \"BUY\" order will only be executed if the Stochastic RSI is below the decided level."
ttstochrsilevel     = "A \"BUY\" order can only be executed if the Stochastic RSI is below this level."
ttlengthRSI         = "The price action of every asset is different, so the Stochastic RSI must be tuned and timed with the market.\nTaking the time to adjust this value will have a great impact on profitability."
ttlengthStoch       = "The Stochastic length should typically be slightly longer than the RSI length. After adjusting all settings, start from the top and do it again.\nRepeatedly tuning this indicator from top to bottom will give you the best results."
ttbuystring         = "Insert your custom alert message for placing a \"BUY\" order here.\nIf you're using a 3Commas bot, insert the \"Deal Start\" message here with a forward slash before each quotation.\nSelect \"Alert() function calls only\" in the alert options."
ttsellstring        = "Insert your custom alert message for placing a \"SELL\" order here.\nIf you're using a 3Commas bot, insert the \"Deal Close\" message here with a forward slash before each quotation.\nSelect \"Alert() function calls only\" in the alert options."
tttakestring        = "Insert your custom alert message for placing a \"TAKE\" order here.\nIf you're using a 3Commas bot, insert the \"Deal Close\" message here with a forward slash before each quotation.\nSelect \"Alert() function calls only\" in the alert options."
ttstopstring        = "Insert your custom alert message for placing a \"STOP\" order here.\nIf you're using a 3Commas bot, insert the \"Deal Close\" message here with a forward slash before each quotation.\nSelect \"Alert() function calls only\" in the alert options."
ttexpirestring      = "Insert your custom alert message for placing a \"EXPIRE\" order here.\nIf you're using a 3Commas bot, insert the \"Deal Close\" message here with a forward slash before each quotation.\nSelect \"Alert() function calls only\" in the alert options."

//Options///////////////////////////////////////////////////////////////////////
tradetrendoption    = input(false, title="Only Tade with Trend", group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=tttradetrend)
sellaftertrend      = input(false, title="Sell After Trend Reverses", group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttsellaftertrend)
sellout             = input.int(title="Sell After (bars)",    defval=10,  minval=0,   maxval=10000, group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttsellout)
sellinprofitoption  = input(true,  title="Only Sell in Profit",  group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttsellinprofit)
minimumprofit       = input.float(title="Minimum Profit (%)", defval=3.5, minval=0,   maxval=100,  step=.1, group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttminimumprofit) / 100
usetakeprofitoption = input(true,  title="Use Take Profit",      group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttusetakeprofit)
takeprofitpercent   = input.float(title="Take Profit (%)",    defval=11.5,  minval=0,   maxval=1000, step=.1, group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=tttakeprofitpercent) / 100
usestoplossoption   = input(true,  title="Use Stop Loss",        group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttusestoploss)
stoplosspercent     = input.float(title="Stop Loss (%)",      defval=-7.5,  minval=-50, maxval=0,    step=.1, group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttstoplosspercent) / 100
usetradeexpiration  = input(true, title="Use Trade Expiration", group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttexpireoption)
expirationtime      = input.int(title="Expire After (bars)",  defval=158,  minval=1,   maxval=10000, group="𝐓𝐑𝐀𝐃𝐄 𝐎𝐏𝐓𝐈𝐎𝐍𝐒", tooltip=ttexpiretime)

//Moving Averages///////////////////////////////////////////////////////////////
src = close
ma(source, length, type) =>
     type == "SMA"  ? ta.sma(source, length) :
     type == "EMA"  ? ta.ema(source, length) :
     type == "RMA"  ? ta.rma(source, length) :
     type == "HMA"  ? ta.wma(2*ta.wma(source, length/2)-ta.wma(source, length), math.floor(math.sqrt(length))) :
     type == "WMA"  ? ta.wma(source, length) :
     type == "VWMA" ? ta.vwma(source, length) :
     na

//MA1
ma1_type   = input.string("RMA", "MA 1", inline="MA 1", options=["SMA", "EMA", "RMA", "HMA", "WMA", "VWMA"], group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒")
ma1_length = input.int(7, "", inline="MA 1", minval=1, group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒", tooltip=ttma1)
ma1 = ma(src, ma1_length, ma1_type)
ma1line = plot(ma1, color=color.blue, linewidth=2, title="MA 1")
//MA2
ma2_type   = input.string("HMA", "MA 2", inline="MA 2", options=["SMA", "EMA", "RMA", "HMA", "WMA", "VWMA"], group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒")
ma2_length = input.int(54, "", inline="MA 2", minval=1, group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒", tooltip=ttma2)
ma2 = ma(src, ma2_length, ma2_type)
ma2line = plot(ma2, color=color.purple, linewidth=2, title="MA 2")
fillcolor = ma1 > ma2 ? color.blue : color.purple
fill(ma1line, ma2line, title="EMA Fill", color=color.new(fillcolor, 80), editable=true)
//MA3
ma3_type   = input.string("EMA", "MA 3", inline="MA 3", options=["SMA", "EMA", "RMA", "HMA", "WMA", "VWMA"], group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒")
ma3_length = input.int(200, "", inline="MA 3", step=5, minval=10, group="𝐌𝐎𝐕𝐈𝐍𝐆 𝐀𝐕𝐄𝐑𝐀𝐆𝐄𝐒", tooltip=ttma3)
ma3 = ma(src, ma3_length, ma3_type)
trendcolor = ma3 > ma3[1] ? color.blue : color.purple
ma3line = plot(ma3, color=trendcolor, linewidth=2, title="MA 3")

//Stochastic RSI////////////////////////////////////////////////////////////////
usestochrsi = input(true, title="Use Stoch RSI", group="𝐒𝐓𝐎𝐂𝐇𝐀𝐒𝐓𝐈𝐂 𝐑𝐒𝐈", tooltip=ttusestochrsi)
stochrsilevel = input.int(defval=61, minval=5, maxval=95, title="Stoch RSI Less Than", group="𝐒𝐓𝐎𝐂𝐇𝐀𝐒𝐓𝐈𝐂 𝐑𝐒𝐈", tooltip=ttstochrsilevel)
lengthRSI = input.int(12, "RSI Length", minval=1, group="𝐒𝐓𝐎𝐂𝐇𝐀𝐒𝐓𝐈𝐂 𝐑𝐒𝐈", tooltip=ttlengthRSI)
lengthStoch = input.int(20, "Stoch Length", minval=1, group="𝐒𝐓𝐎𝐂𝐇𝐀𝐒𝐓𝐈𝐂 𝐑𝐒𝐈", tooltip=ttlengthStoch)
rsi1 = ta.rsi(src, lengthRSI)
smoothK = 3
k = ta.sma(ta.stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)

//Buy Sell Conditions///////////////////////////////////////////////////////////
buy          = ma1 > ma2
buystochrsi  = buy and k < stochrsilevel
buywithtrend = buy and ma3 > ma3[1]
buystochrsitrue = usestochrsi      ? buystochrsi  : buy
buytrendtrue    = tradetrendoption ? buywithtrend : buy
buyoption    = buystochrsitrue and buytrendtrue

mpconvert    = strategy.position_avg_price * (1 + minimumprofit)
mpnarrow     = mpconvert < close and strategy.openprofit > 0
sell         = ma1 < ma2
sellinprofit = sell and mpnarrow
selloption   = sellaftertrend ? ma3 < ma3[sellout] or (sellinprofitoption ? sellinprofit : sell) : (sellinprofitoption ? sellinprofit : sell)

take         = strategy.position_avg_price * (1 + takeprofitpercent)
takeoption   = take < close and usetakeprofitoption

stop         = strategy.position_avg_price * (1 + stoplosspercent)
stopoption   = stop > close and usestoplossoption

//The code below extends the expiration to 1,000,000 bars if expiration is disabled. This ensures that no trade will expire.
tradeexpireextend   = usetradeexpiration ? expirationtime : 1000000
expirereduction     = ma3 < ma3[1] ? tradeexpireextend / 2 : tradeexpireextend

//Alternate Labels and Expire///////////////////////////////////////////////////
//Don't Repeat Buy or Sell signals
var pos = 0
if buyoption and pos <= 0
    pos := 1
if selloption or stopoption or takeoption and pos >= 0
    pos := -1
buypos  = pos ==  1 and (pos !=  1)[1]
sellpos = pos == -1 and (pos != -1)[1]

//Expire Conditions and Declare Position to be the same as a sell position.
expire = ta.barssince(buypos) > tradeexpireextend
if expire and pos >= 0
    pos := -1
expirepos = pos == -1 and (pos != -1)[1] and expire

//Sell Only Applies if Other Close Conditions are False
sellvsother = stopoption or takeoption or expire ? na : sellpos

//Finalize Signals//////////////////////////////////////////////////////////////
buyfinal    = buypos
sellfinal   = sellvsother
takefinal   = takeoption
stopfinal   = stopoption
expirefinal = expirepos

//Trades////////////////////////////////////////////////////////////////////////
if buyfinal
	strategy.entry("Long Position", strategy.long, comment="BUY")
if sellfinal
	strategy.close("Long Position", comment="SELL")
if takefinal
    strategy.close("Long Position", comment="TAKE")
if stopfinal
    strategy.close("Long Position", comment="STOP")
if expirefinal
    strategy.close("Long Position", comment="EXPIRE")

//Plot Labels///////////////////////////////////////////////////////////////////
plotshape(buyfinal,    style=shape.labelup,   location=location.belowbar, color=color.blue,   text="𝐁𝐔𝐘",       textcolor=color.white, size=size.tiny)
plotshape(sellfinal,   style=shape.labeldown, location=location.abovebar, color=color.purple, text="𝐒𝐄𝐋𝐋",     textcolor=color.white, size=size.tiny)
plotshape(takefinal,   style=shape.labeldown, location=location.abovebar, color=color.black,  text="𝐓𝐀𝐊𝐄",     textcolor=#26a69a,     size=size.tiny)
plotshape(stopfinal,   style=shape.labelup,   location=location.belowbar, color=color.black,  text="𝐒𝐓𝐎𝐏",     textcolor=#ef5350,     size=size.tiny)
plotshape(expirefinal, style=shape.labeldown, location=location.abovebar, color=color.black,  text="𝐄𝐗𝐏𝐈𝐑𝐄", textcolor=#ffeb3b,     size=size.tiny)

//Alerts////////////////////////////////////////////////////////////////////////
usebuyalert    = input(defval=true, title="Use BUY Alert",     group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
buystring      = input.string(title="Buy Alert Message",    defval="BUY",    confirm=false, group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒", tooltip=ttbuystring)
usesellalert   = input(defval=true, title="Use SELL Alert",                                 group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
sellstring     = input.string(title="Sell Alert Message",   defval="SELL",   confirm=false, group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒", tooltip=ttsellstring)
usetakealert   = input(defval=true, title="Use TAKE Alert",                                 group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
takestring     = input.string(title="Take Alert Message",   defval="TAKE",   confirm=false, group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒", tooltip=tttakestring)
usestopalert   = input(defval=true, title="Use STOP Alert",                                 group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
stopstring     = input.string(title="Stop Alert Message",   defval="STOP",   confirm=false, group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒", tooltip=ttstopstring)
useexpirealert = input(defval=true, title="Use EXPIRE Alert",                               group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒")
expirestring   = input.string(title="Expire Alert Message", defval="EXPIRE", confirm=false, group="𝐀𝐋𝐄𝐑𝐓 𝐌𝐄𝐒𝐒𝐀𝐆𝐄𝐒", tooltip=ttexpirestring)

if buyfinal and usebuyalert
	alert(buystring,    alert.freq_once_per_bar)
if sellfinal and usesellalert
	alert(sellstring,   alert.freq_once_per_bar)
if takefinal and usetakealert
    alert(takestring,   alert.freq_once_per_bar)
if stopfinal and usestopalert
    alert(stopstring,   alert.freq_once_per_bar)
if expirefinal and useexpirealert
    alert(expirestring, alert.freq_once_per_bar)

//BOT Instructions//////////////////////////////////////////////////////////////

//In the Indicator Setting Inputs Tab, do the following...
//Format your 3Commas messages to work with pine script.
//Replace the "BUY" message with your 3Commas "Deal Start" message.
//Replace the "SELL" and "STOP" messages with your 3Commas "Deal Close" message.

//In the Alert Settings, do the following...
//Condition = "𝐉𝐔𝐈𝐂𝐘 𝐓𝐑𝐄𝐍𝐃" and "alert() function calls only".
//Expiration time = Maximum time possible.
//Alert actions = Webhook URL (provided by 3Commas)
//3Commas BOT will receive the messages and initiate trades accordingly.




