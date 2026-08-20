/*
 * Problem:    <Problem Title>
 * Platform:   LeetCode
 * Link:       https://leetcode.com/problems/distribute-elements-into-two-arrays-i/description/?envType=daily-question&envId=2026-08-20
 * Difficulty: Easy
 * Topics:     Arrays, Hashing
 *
 * Approach:
 *   -
 *
 * Complexity:
 *   Time:  O(?)
 *   Space: O(?)
 */

#include <bits/stdc++.h>
using namespace std;

// ─── Solution ────────────────────────────────────────────────────────────────

class Solution {
public:
    vector<int> resultArray(vector<int>& nums) {
        vector<int> arr1;
        vector<int> arr2;
        vector<int> result;
        arr1.push_back(nums[0]);
        arr2.push_back(nums[1]);
        int n = 2;
        int a = 0; int b = 0;

        for(int i = n; i<nums.size(); i++){
            if(arr1[a] > arr2[b]){
                arr1.push_back(nums[i]);
                a++;
            }else{
                arr2.push_back(nums[i]);
                b++;
            }
        }

        for(int i = 0; i<arr1.size(); i++){
            result.push_back(arr1[i]);
        }
        for(int i = 0; i<arr2.size(); i++){
            result.push_back(arr2[i]);
        }

        return result;
    }
};

