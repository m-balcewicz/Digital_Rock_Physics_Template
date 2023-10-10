function data = exchange2matlab(path, dimension)

% This function is used to import data from a uint8-file and reshape it to the original shape.
% 04/2023
% Martin Balcewicz (martin.balcewicz@rockphysics.org)

%% Import Data
% Define the shape of the data
if ~isempty(dimension)
x_size = dimension;
y_size = dimension;
z_size = dimension;
else
error('No dimension was set!');
end

% Read the data from the file
fid = fopen(path, 'rb');
data = fread(fid, inf, 'uint8=>uint8');
fclose(fid);

% Reshape the data to the original shape
data = reshape(data, [z_size, x_size, y_size]);

% IMPORTANT: due to reading automations of arrays the final array's
% columns must be flipped to fit the original data set!
data = flip(data,3);

slice = dimension/2;

%% Make Figure XY in Z direction
F1 = figure('Name','Segmented CT Image','NumberTitle','off');
pcolor(data(:,:,slice))
axis tight;
shading interp;
colorbar('v');
clear i
set(F1,'renderer','zbuffer')
title('XY')
% set(gca, 'XDir', 'reverse')
hold on
annotation('textbox',[0.145, 0.08, .2, .2], 'String', ['slicenumber : ',num2str(slice)],'BackgroundColor','white','FitBoxToText','on','LineWidth',.5,'HorizontalAlignment','center','VerticalAlignment','middle');
set(findall(F1,'-property','FontSize'),'FontSize',12)

end

