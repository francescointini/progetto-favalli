var tabel= document.getElementById("tabella1");

var n=100;
var i,j=0;
for(i=0;i<=n;i++)
{
   document.write("<tr>");
   for(j=0;j<3;j++)
   {
       document.write("<td>");
       if(i==0 && j==0)
       {
           document.write("N operazione:");
       }
       else if(i==0 && j==1)
       {
           document.write("Risultato macchina faulty:");
       }
       else if(i==0 && j==2)
       {
           document.write("Risultato macchina fault-free:");
       }
       else if(i!=0 && j==0)
       {
            document.write(i);
       }
       else if(i!=0 && j==1)
       {
           document.write("Risultato macchina 1");
       }
       else if(i!=0 && j==2)
       {
           document.write("Risultato macchina 2");
       }
       document.write("</td>");
   }
   document.write("</tr>");
}
document.close();
