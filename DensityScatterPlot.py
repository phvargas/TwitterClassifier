from Utilities.Sorting import dictionaryByValue
from twitter_apps.Subjects import get_values
import plotly.graph_objs as go
import plotly
from scipy import stats
from numpy import array

plotly.offline.init_notebook_mode(connected=True)

tweet_density = {'mitchellreports': 4.258555133079848, 'jdickerson': 2.9904127961849882, 'aglynch': 2.748562348668281,
                 'sarahpalinusa': 2.4472946334074024, 'Jonahnro': 4.368805909209012, 'LarrySabato': 2.9738562091503264,
                 'michelleobama': 2.9028040502948707, 'donnabrazile': 4.156347582642404, 'maddow': 6.904231625835189,
                 'marthamaccallum': 2.3628454755282005, 'mattyglesias': 3.4041675263049314,
                 'chrislhayes': 6.619774235634466, 'judgenap': 2.2924525975787162, 'anncurry': 2.1855054391520503,
                 'lawrence': 6.768109050562689, 'chriscuomo': 3.9972125435540065, 'kirstenpowers': 3.606366459627329,
                 'morningmika': 3.1382978723404253, 'mharrisperry': 3.641999225106548, 'lydiacachosi': 6.681190994916484,
                 'gloriasteinem': 2.3324638844301764, 'tuckercarlson': 1.9453642384105958, 'JoeNBC': 4.220785236515907,
                 'markos': 13.257575757575758, 'mkhammer': 3.4319592507028136, 'glennbeck': 2.095362089135439,
                 'daveweigel': 4.8641571194762685, 'ShepNewsTeam': 2.2165192138853245,
                 'hillaryclinton': 3.0029474261429843, 'juliaioffe': 3.3762993762993765,
                 'michellemalkin': 3.3144567131953253, 'anncoulter': 7.343870470316115, 'GeorgeWill': 2.121158999273747,
                 'tanehisicoates': 2.3634453781512605, 'megynkelly': 3.2779009608277896, 'RBReich': 2.4320659260418296,
                 'ericbolling': 2.3811569301260023, 'NateSilver538': 4.023653828103001, 'paulkrugman': 3.457162306719829,
                 'ggreenwald': 9.105153203342619, 'AshleyJudd': 4.2063492063492065, 'anamariecox': 8.945054945054945,
                 'tomfriedman': 2.1052631578947367, 'ariannahuff': 2.1556122448979593, 'mtaibbi': 2.270492448080554,
                 'brithume': 3.3255912162162162, 'andylevy': 15.357142857142858, 'katyturnbc': 5.590881258537045,
                 'DineshDSouza': 5.390753990093561, 'costareports': 4.675245098039216, 'aparnapkin': 4.69920787839863,
                 'AnneBayefsky': 2.207543149371404, 'jaketapper': 3.9894191319369465, 'nickkristof': 4.55207344096233,
                 'secupp': 2.989270607655009, 'pamelageller': 2.4356995884773665, 'billoreilly': 2.100202429149798,
                 'harrisfaulkner': 7.401869158878505, 'connieschultz': 2.9087292018326503,
                 'davidfolkenflik': 11.755485893416928, 'BarackObama': 2.196340713407134,
                 'kathygriffin': 2.9221945188331744, 'nycjim': 4.2604180535215015, 'BernieSanders': 3.9814569201813885,
                 'gstephanopoulos': 2.0377776078380214, 'AsiaArgento': 11.551411551411551,
                 'AriMelber': 3.876625135427952, 'TeamCavuto': 3.2042520880789676, 'tomilahren': 3.8067598160947056,
                 'krauthammer': 1.9757291014843612, 'jemelehill': 3.9863250132766863, 'dianesawyer': 2.8952256090899158,
                 'trevornoah': 3.0685570013594874, 'dloesch': 4.648033914654888, 'ewerickson': 8.48532028469751,
                 'ehasselbeck': 3.6828036828036828, 'katiecouric': 2.9518072289156625,
                 'kimguilfoyle': 2.8536135347280855, 'iowahawkblog': 8.695652173913043, 'MEPFuller': 4.78573937478047,
                 'donlemon': 3.2748945392623554, 'capehartj': 2.8619771041831665, 'tavissmiley': 4.0087463556851315,
                 'thereval': 2.9437391087876525, 'richlowry': 10.232843137254902, 'fredbarnes': 1.9761949744946155,
                 'seanhannity': 2.470885845165113, 'edhenry': 3.288412261554522, 'billkeller2014': 5.1020408163265305,
                 'greta': 2.3307790549169862, 'majorcbs': 3.257575757575758, 'fareedzakaria': 2.584915084915085,
                 'HardballChris': 8.311024580189827, 'ClaireAForlani': 6.869834710743801,
                 'Peggynoonannyc': 8.00955068374213, 'ahmalcolm': 3.007346189164371, 'monicacrowley': 3.276848838514196,
                 'BetsyDeVos': 4.958602492948776, 'lesdoggg': 2.4362719065321294, 'danaperino': 4.254278728606357,
                 'ingrahamangle': 2.8918938255705804, 'andersoncooper': 4.358634126677528,
                 'davidfrum': 3.1046181044986505, 'michaelsmith': 6.4478986758779495,
                 'katrinanation': 12.931034482758621, 'andreatantaros': 2.216673887102781,
                 'camanpour': 2.619321082184788, 'amberinzaman': 7.130281690140845, 'kilmeade': 2.1054907047124947,
                 'sullydish': 2.908016807421891, 'iamsambee': 15.80547112462006, 'maureendowd': 2.8680161943319837,
                 'britmarling': 3.6797184996630983, 'davidcorndc': 3.3024938685316045, 'oprah': 3.591733870967742,
                 'billhemmer': 4.030518284661931, 'iamjohnoliver': 2.008320992877794, 'bretbaier': 8.04289544235925,
                 'charlesmblow': 4.299149126735333, 'greggutfeld': 3.0577458256029684}


deleted_density = {'greta': 5.476190476190476, 'BetsyDeVos': 4.497354497354497, 'trevornoah': 4.987980769230769,
                   'LarrySabato': 15.384615384615385, 'HardballChris': 19.047619047619047,
                   'seanhannity': 2.70509977827051, 'lawrence': 11.5, 'amberinzaman': 18.333333333333332,
                   'oprah': 4.874835309617918, 'dloesch': 5.366161616161616, 'monicacrowley': 7.258064516129033,
                   'davidfrum': 4.7023809523809526, 'harrisfaulkner': 13.125, 'ewerickson': 14.347826086956522,
                   'ariannahuff': 33.33333333333333, 'tomfriedman': 4.941660947151681, 'gloriasteinem': 10.15625,
                   'ingrahamangle': 3.5114503816793894, 'chriscuomo': 8.518518518518519, 'michaelsmith': 29.166666666666668,
                   'hillaryclinton': 3.415814954276493, 'mitchellreports': 9.615384615384617,
                   'anncurry': 12.5, 'mtaibbi': 5.238095238095238, 'juliaioffe': 5.705996131528046,
                   'danaperino': 6.938020351526363, 'TeamCavuto': 5.934343434343434, 'connieschultz': 13.88888888888889,
                   'judgenap': 3.634085213032581, 'AriMelber': 7.936507936507936, 'britmarling': 8.630952380952381,
                   'RBReich': 3.1301145662847794, 'ehasselbeck': 0, 'bretbaier': 11.574074074074074,
                   'majorcbs': 13.333333333333334, 'richlowry': 20.833333333333336, 'greggutfeld': 3.9619047619047616,
                   'ClaireAForlani': 25.0, 'mharrisperry': 33.33333333333333, 'davidfolkenflik': 100.0,
                   'aglynch': 3.624338624338624, 'billkeller2014': 100.0, 'andylevy': 50.0,
                   'brithume': 4.550084889643464, 'katrinanation': 0, 'chrislhayes': 9.44055944055944,
                   'GeorgeWill': 5.747126436781609, 'michellemalkin': 6.493506493506493,
                   'BarackObama': 2.235217673814165, 'lydiacachosi': 37.5, 'ShepNewsTeam': 7.449494949494949,
                   'katiecouric': 12.121212121212121, 'billhemmer': 20.0, 'camanpour': 8.630952380952381,
                   'jemelehill': 5.420054200542006, 'markos': 100.0, 'marthamaccallum': 5.236547490068617,
                   'kilmeade': 7.552083333333333, 'andreatantaros': 3.7943696450428397,
                   'BernieSanders': 4.209183673469387, 'davidcorndc': 4.7272727272727275,
                   'tanehisicoates': 9.285714285714286, 'mattyglesias': 7.177033492822966,
                   'donlemon': 3.430232558139535, 'glennbeck': 4.21455938697318, 'costareports': 13.333333333333334,
                   'krauthammer': 3.747221340107971, 'JoeNBC': 4.646464646464646, 'AshleyJudd': 15.357142857142858,
                   'DineshDSouza': 5.733397037744864, 'jdickerson': 18.333333333333332, 'fredbarnes': 33.33333333333333,
                   'anamariecox': 33.33333333333333, 'billoreilly': 2.2055137844611528, 'maureendowd': 6.486486486486487,
                   'thereval': 8.823529411764707, 'iamjohnoliver': 2.4489795918367347,
                   'kirstenpowers': 5.277777777777778, 'nickkristof': 12.142857142857142,
                   'paulkrugman': 8.658008658008658, 'ahmalcolm': 50.0, 'sarahpalinusa': 3.55718085106383,
                   'mkhammer': 8.923076923076923, 'charlesmblow': 5.571847507331378, 'katyturnbc': 8.333333333333332,
                   'morningmika': 4.06026557711951, 'Peggynoonannyc': 32.5, 'kathygriffin': 3.8666666666666667,
                   'secupp': 5.6878306878306875, 'iowahawkblog': 11.11111111111111, 'andersoncooper': 4.68509984639017,
                   'aparnapkin': 9.429280397022332, 'capehartj': 12.345679012345679, 'edhenry': 9.523809523809524,
                   'maddow': 7.322929171668667, 'nycjim': 16.666666666666664, 'michelleobama': 3.3157894736842106,
                   'ggreenwald': 18.75, 'tavissmiley': 50.0, 'kimguilfoyle': 3.7786774628879893,
                   'donnabrazile': 8.092948717948719, 'anncoulter': 7.5706214689265545, 'dianesawyer': 6.696428571428571,
                   'AnneBayefsky': 10.084033613445378, 'jaketapper': 6.082589285714286,
                   'gstephanopoulos': 3.4133333333333336, 'tomilahren': 4.867788461538462,
                   'NateSilver538': 4.862119013062409, 'MEPFuller': 16.666666666666664, 'lesdoggg': 5.244755244755245,
                   'pamelageller': 4.425446316318833, 'sullydish': 11.904761904761903, 'iamsambee': 50.0,
                   'fareedzakaria': 7.03448275862069, 'Jonahnro': 9.27536231884058, 'tuckercarlson': 1.943039659302635,
                   'daveweigel': 10.119047619047619, 'AsiaArgento': 25.0, 'ericbolling': 2.873015873015873,
                   'megynkelly': 4.621848739495799}



x_conservative = []
y_conservative = []
text_conservative = []

x_liberal = []
y_liberal = []
text_liberal = []

x_other = []
y_other = []
text_other = []

x_all = []
y_all = []

x_male = []
y_male = []
text_male = []

x_female = []
y_female = []
text_female = []

for handle, magnitude in dictionaryByValue(tweet_density):
    subject = get_values(handle=handle)[0]
    print(subject['name'])

    x_all.append(magnitude)
    y_all.append(deleted_density[handle])
    
    if subject['sex'] == 'male':
        text_male.append(subject['name'])
        x_male.append(magnitude)
        y_male.append(deleted_density[handle])

    else:
        text_female.append(subject['name'])
        x_female.append(magnitude)
        y_female.append(deleted_density[handle])

    if subject['stance'] == 'conservative':
        text_conservative.append(subject['name'])

        x_conservative.append(magnitude)
        print('x:', magnitude)

        y_conservative.append(deleted_density[handle])
        print('y:', deleted_density[handle])
    elif subject['stance'] == 'liberal':
        text_liberal.append(subject['name'])

        x_liberal.append(magnitude)
        print('x:', magnitude)

        y_liberal.append(deleted_density[handle])
        print('y:', deleted_density[handle])
    else:
        text_other.append(subject['name'])

        x_other.append(magnitude)
        print('x:', magnitude)

        y_other.append(deleted_density[handle])
        print('y:', deleted_density[handle])

# Generated linear fit
xi = array([0, max(x_all)])
slope, intercept, r_value, p_value, std_err = stats.linregress(x_all, y_all)
line = slope * xi + intercept

trace1 = go.Scatter(
    x=x_conservative,
    y=y_conservative,
    mode='markers',
    name='Conservative',
    text=text_conservative,
    marker=dict(
        color='rgba(255,0,0,.8)'
    ),
)

trace2 = go.Scatter(
    x=x_liberal,
    y=y_liberal,
    mode='markers',
    name='Liberal',
    text=text_liberal,
    marker=dict(
        color='rgba(40,119,175,.8)'
    ),
)

trace3 = go.Scatter(
    x=x_other,
    y=y_other,
    mode='markers',
    name='Other',
    text=text_other,
    marker=dict(
        color='rgba(0,255,0,.8)'
    ),
)

trace0 = go.Scatter(
    x=xi,
    y=line,
    mode='line',
    name='Fit',
    marker=dict(
        color='rgb(211, 211, 211)'
    ),
)

layout = go.Layout(
    title='Conversation Tweets Density &<br>Deleted Conversation Tweets Density Relation<br>Political Stance View',
    font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
    xaxis=dict(
        title='Conversation Tweet Density',
        titlefont=dict(
            family='Courier New, monospace',
            size=16,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Conversation Deleted Tweet Density',
        titlefont=dict(
            family='Courier New, monospace',
            size=16,
            color='#7f7f7f'
        )
    )
)

data = [trace0, trace1, trace2, trace3]
fig = go.Figure(data=data, layout=layout)

plotly.offline.plot(fig, filename='Plotly/political-scatterplot.html', auto_open=True)

trace1 = go.Scatter(
    x=x_male,
    y=y_male,
    mode='markers',
    name='Male',
    text=text_male,
    marker=dict(
        color='rgba(40,119,175,.8)'
    ),
)

trace2 = go.Scatter(
    x=x_female,
    y=y_female,
    mode='markers',
    name='Female',
    text=text_female,
    marker=dict(
        color='rgba(255,20,147,.8)'
    ),
)

layout = go.Layout(
    title='Conversation Tweets Density &<br>Deleted Conversation Tweets Density Relation<br>View by Sex',
    font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'),
    xaxis=dict(
        title='Conversation Tweet Density',
        titlefont=dict(
            family='Courier New, monospace',
            size=16,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Conversation Deleted Tweet Density',
        titlefont=dict(
            family='Courier New, monospace',
            size=16,
            color='#7f7f7f'
        )
    )
)

data = [trace0, trace1, trace2]
fig = go.Figure(data=data, layout=layout)

# plotly.offline.plot(fig, filename='Plotly/bySex-scatterplot.html', auto_open=True)