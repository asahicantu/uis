
hr=[1 0 -1];
hc=[1 0 -1]';

der_r_c=conv2(hr,hc)
sr=[1/4 2/4 1/4]
sc=[1/4 2/4 1/4]'
sm_r_c=conv2(sr,sc)  % 2D gauss

filt1=conv2(der_r_c,sm_r_c)

Filt2=conv2(conv2(hr,sc),conv2(sr,hc))

I= imread('cameraman.tif');
I2=imfilter(I,filt1);

figure(1)
subplot(3,2,1)
imshow(I)
title('original')
subplot(3,2,2)
title('smooth both direction + derivative in both direction')
subplot(3,2,3)
Ismooth=imfilter(I,sm_r_c)
imshow(Ismooth)
title('smooth both direction')
subplot(3,2,4)
Ider=imfilter(I,der_r_c)
imshow(Ider)
title('derovative both direction')
subplot(3,2,5)
Idc=imfilter(I,conv2(sr,hc))
imshow(Idc)
title('derovative over column, smooth over row')
subplot(3,2,6)
Idr=imfilter(I,conv2(hr,sc))
imshow(Idr)
title('derovative over row, smooth over column')

%----  

%Sobel of larger filter kernels 

%Just additinal smooting... 
    


f1=conv2(hr,sc)
conv2(f1,conv2(sc,sr))

