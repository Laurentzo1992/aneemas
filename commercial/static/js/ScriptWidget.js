ChartGeneratorCH0001SW6 = function(sid) {
  this.sid = sid;
  this.containerId = "brtChart_" + sid;

  if ('')
    this.containerId = '';   

  this.tmz_shift = "0";
}

ChartGeneratorCH0001SW6.prototype = {

    trimAll: function(sString) {
        return (String(sString)).replace(/^\s*/, "").replace(/\s*$/, "");
    },

    CheckSiteLink: function(link) {
        if (
          (link.style.display    == 'none') ||
          (link.style.visibility == 'hidden')
         ) {
            return false;
        }

        var obj = link;
        if (obj.parentNode) {
            while (obj.parentNode) {
                if ((obj.style.display == 'none') ||
                  (obj.style.visibility == 'hidden')
                  )
                    return false;

                obj = obj.parentNode;
            }
        }

        return true;
    },

    GetDoc : function () {
      return top.document;
    },


    CheckCrossDomainIssue: function() {
        var doc;
        try {
            doc = this.GetDoc();
            if (doc.body.innerHTML)
            { }
        }
        catch (e) {
            return false;
        }

        return true;
    },

    AreLinksEqual: function(l1, l2) {
        l1 = l1.toLowerCase();
        l2 = l2.toLowerCase();

        l1 = l1.replace("www.", "");
        l2 = l2.replace("www.", "");
        l1 = l1.replace("http://", "");
        l1 = l1.replace("https://", "");
        l2 = l2.replace("http://", "");
        l2 = l2.replace("https://", "");

        return l1.indexOf(l2) == 0;
    },

    ExtractDomain: function() {
        var d = 'https://www.bullion-rates.com/';

        return d.toLowerCase().replace("http://", "").replace("https://", "").replace(/\/.*/, ''); 
    },

    IsSiteLinkCorrect: function(cLink) {
        if (!cLink)
          return false;

        var link = ("https://www.bullion-rates.com/").toLowerCase();
        link = link.substring(0, link.length - 1);


        if (this.AreLinksEqual(cLink.href, link)) {
            return this.CheckSiteLink(cLink);
        }
        return false;
    },

    GenerateHtml: function() {

        if (!this.CheckCrossDomainIssue()) {
            var c = document.getElementById(this.containerId);
            if (!c)
                alert("container for rates table was not found");
            else
                c.innerHTML = "<b>ERROR: You are using FRAME or IFRAME with custom content to load it on the main page with the different domain name.<br />This is not supported.<br />Please place custom content on the main page directly.</b>";
            return;
        }

        var c = document.getElementById(this.containerId);

        if (!this.IsSiteLinkCorrect(c)) {
            if (!c)
                alert("container for rates table was not found");
            else
                c.innerHTML = "<b>ERROR: A visible link to &lt;a&nbsp;href=\"https://www.bullion-rates.com/\"&gt;" + this.ExtractDomain() + "&lt;/a&gt; is required to use this content.</b>";
            return;
        }

        var control = this.GetWidgetContent();
        if (!c)
            alert("container for chart was not found");
        else
            c.appendChild(control);

        this.InitGARequest();  
    },

    GetWidgetContent: function() {
        var title  = 'Gold Prices in CFA BCEAO Francs (price per kilogram)';
        var width  = '504px';
        var height = '320px';
        var url    = 'https://www.bullion-rates.com/gold/XOF/SpotPrice-chart.png?sid=CH0001SW6&fi=6%7c0%7c0&exp=TzXGn4qGbartUwy3iBgYZsJabC5dv5xuVEfuAAN%2bHYU%3d&stk=-05TXYF41CQ';

        url += (url.indexOf('?') == -1 ? "?" : "&") + "ts=" + (-1 * (this.tmz_shift != "" ? Number(this.tmz_shift) : new Date().getTimezoneOffset())).toString();
        
        var control = document.createElement("IMG");
        control.setAttribute("alt",    title);
        control.setAttribute("width",  width);
        control.setAttribute("height", height);
        control.setAttribute("src",    url);
        control.setAttribute("border", "0");

        return control;
    },

    GetRnd: function () { return Math.floor(Math.random()*1000000001); },
    GetRnd2: function () { return Math.floor(Math.random()*2147483647); },
    GetUtmccn: function (ur) {
     if (ur=="0" || ur=="" || ur=="-") return "";
     var i=0,h,k,n;
     if ((i=ur.indexOf("://"))<0) return "";
     h=ur.substring(i+3,ur.length);
     if (h.indexOf("/") > -1) 
     {
       k=h.substring(h.indexOf("/"),h.length);
       if (k.indexOf("?") > -1) 
         k=k.substring(0,k.indexOf("?"));
       h=h.substring(0,h.indexOf("/"));
     }
     h=h.toLowerCase();
     n=h;
     if ((i=n.indexOf(":")) > -1) 
       n=n.substring(0,i);
     if (h.indexOf("www.")==0) 
       h=h.substring(4,h.length);
     return "utmccn=(referral)|utmcsr="+this.uEscape(h)+"|"+"utmcct="+this.uEscape(k)+"|utmcmd=referral";
    },
    uEscape: function (s) { return escape(s); 
    },    

    InitGARequest: function ()
    {
      var var_utmac      = 'UA-23864840-3';                      // --
      var var_utmhn      = escape('test5.mbhmedia.net');         //
      var var_utmn       = this.GetRnd();                        //random request number
      var var_cookie     = this.GetRnd();                        //random cookie number
      var var_random     = this.GetRnd2();                       //number under 2147483647
      var var_today      = Number(new Date());                   //today
      var var_referer    = this.uEscape(location);               //referer url    -- Page on which content is loaded

      var var_uservar    = '-';                              //enter your own user defined variable
      var var_utmp       = this.uEscape('/chartwidget.htm?sub=www&type=Day24Hours&sid=CH0001SW6'); // This is the page -- GetCustomContent.aspx?...

      var url =  ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + 
                 '.google-analytics.com/__utm.gif?utmwv=1.1&utmn=' + var_utmn + 
                 '&utmcs=utf-8&utmsr=1280x1024' + 
                 '&utmsc=32-bit&utmul=en-us&utmje=1&utmfl=9.0&utmdt=Exchange%20Rates&utmhn=' + var_utmhn + 
                 '&utmhid=' + var_random +
                 '&utmr=' + var_referer + 
                 '&utmp=' + var_utmp    + 
                 '&utmac=' + var_utmac  + 
                 '&utmcc=__utma%3D' + var_cookie + '.' + var_random + '.' + var_today + '.' + var_today + 
                 '.' + var_today + '.2%3B%2B__utmb%3D' + var_cookie + '%3B%2B__utmc%3D' + var_cookie + 
                 '%3B%2B__utmz%3D' + var_cookie + '.' + var_today + '.2.2.' + 
                  this.uEscape(this.GetUtmccn(location.href)) + '%3b%2b';

      var objImage = new Image(1,1);
      objImage.src = url;
      objImage.onload=function() { _uVoid(); }
    },

    bung: function() { }
}  

function _uVoid () { return; }

var chartGenCH0001SW6 = new ChartGeneratorCH0001SW6('CH0001SW6');
chartGenCH0001SW6.GenerateHtml();