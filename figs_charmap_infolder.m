folder = 'Data';
extention = 'png';
result_separator = ';';


list = dir(strcat(folder, '/*.', extention));
for file = list'
    fname = file.name;
    [filepath,name,ext] = fileparts(file.name);
    imfn = strcat(folder, '/', fname);
%    disp(name);
    im = imread(imfn);
    img = single(rgb2gray(im));
    img = imresize(img, [24 24]);
%-----------------------------------------
    winsz = 24;
    mu = (1/winsz^2) * conv2(img, ones(winsz, winsz, 'single'), 'same');
    x_ = (img - mu).^2;
    stdim = sqrt((1/winsz^2) * conv2(x_, ones(winsz, winsz, 'single'), 'same'));
    data = img - mu;
    eps = 1;
    data = data ./ (stdim + eps);
%-----------------------------------------
    nn = cudaconvnet_to_mconvnet('models/charnet_layers.mat');
    nn = nn.forward(nn, struct('data', data));
    [~,m] = max(nn.Xout, [], 3);
    result = strcat(name, result_separator, int2str(m));
    disp(result);

end

% Max Jaderberg 2014
% Produces character classifier saliency map

%addpath(genpath('./'));
%
%imfn = 'data/img2.jpg';
%im = imread(imfn);
%img = single(rgb2gray(im));
%img = imresize(img, [24 24]);
%
%% pad
%img = padarray(img, [11 11]);

%% preprocess
%winsz = 24;
%mu = (1/winsz^2) * conv2(img, ones(winsz, winsz, 'single'), 'same');
%x_ = (img - mu).^2;
%stdim = sqrt((1/winsz^2) * conv2(x_, ones(winsz, winsz, 'single'), 'same'));
%data = img - mu;
%eps = 1;
%data = data ./ (stdim + eps);

%% load model
%nn = cudaconvnet_to_mconvnet('models/charnet_layers.mat');

%% process
%nn = nn.forward(nn, struct('data', data));

%% fig
%close all;
%fntsz = 20;
%figure(1); 
%subplot(1,2,1); imshow(im);
%subplot(1,2,2);
%[~,m] = max(nn.Xout, [], 3);
%disp(m);
%imshowc(m); caxis([1 37]);
%figure(2); plot(1:length(nn.time), nn.time);
%title('Layer timings');
%xlabel('Layer #');
%ylabel('Time (s)');
%disp(nn.xout)