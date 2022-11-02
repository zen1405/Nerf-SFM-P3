import numpy as np
from scipy import optimize

def Non_Linear_Triangulation(K,P1, P2, X_estimate, inlier_points, X_updated_list = []):
    '''
    P1: Projection matrix of camera 1
    P2: Projection matrix of camera 2
    X_estimate: 3D world coordinate approximations obtained from linear triangulation
    inlier_points: image coordinates (x and x')
    '''
    # Getting matching points in the image
    x_pts = inlier_points[:, 0:2]
    x_dash_pts = inlier_points[:, 2:4]

    for point1, point2, X in zip(x_pts, x_dash_pts, X_estimate):
        X = X.reshape(X.shape[0],-1)
        result = optimize.least_squares(fun=optimizer,x0=X, args=[point1, P1, point2, P2])
        X_updated = result.x
        X_updated = np.reshape(X, (3,))
        X_updated_list.append(X_updated)

    X_updated_list = np.array(X_updated_list)
    X_updated_list = X_updated_list.reshape((X_updated_list.shape[0], 3))

    return X_updated_list

def optimizer(x0, point1, P1, point2, P2, reprojection_error=0):

    #calaculating reprojected point x from camera 1
    x0 = np.reshape(x0, (3, 1))
    x0 = np.vstack((x0, 1))
    x = np.dot(P1, x0)
    x = x/x[2]
    
    #calacualting reprojected point x from camera 1
    x_dash = np.dot(P2, x0)
    x_dash = x_dash/x_dash[2]

    #reprojection error calculation for camera 1 and 2
    reprojection_error += ((point1[0] - x[0])**2) + ((point1[1] - x[1])**2)
    reprojection_error += ((point2[0] - x_dash[0])**2) + ((point2[1] - x_dash[1])**2)

    return reprojection_error