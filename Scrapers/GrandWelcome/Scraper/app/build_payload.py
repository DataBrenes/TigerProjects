from datetime import datetime

def build_pl(rec):
    inTime='04:00PM'
    outTime='10:00AM'
    ch_in=datetime.strptime(rec['Check-In']+' '+inTime, '%b/%d/%Y %I:%M%p').strftime("%Y-%m-%dT%H:%M:%S")
    ch_out=datetime.strptime(rec['Checkout']+' '+outTime, '%b/%d/%Y %I:%M%p').strftime("%Y-%m-%dT%H:%M:%S")
    pl_json={
        "calStart":ch_in,
        "calEnd":ch_out,
        "Summary":rec['Guest'] +" Booking",
        "Description":"A "+str(rec['Nights'])+ ' night booking for '+rec['Guest']+' Reservation ID: '+ str(rec['Res_ID'])
    }
    return pl_json
