import React from 'react';
import { SIGN_IN, SIGN_OUT } from './actiontypes';


export const signIn = (username, password) => {
    return {
        type: SIGN_IN,
        payload: {
            username,
            password
        }
    }
}

export const signOut = (user) => {
    return {
        type: SIGN_OUT,
        payload: user
    }
}
