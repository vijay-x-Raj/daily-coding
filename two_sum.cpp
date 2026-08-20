/*
 * Problem:    Two Sum
 * Platform:   LeetCode
 * Link:       https://leetcode.com/problems/two-sum/
 * Difficulty: Easy
 * Topics:     Arrays, Hashing
 *
 * Approach:
 *   - Use a hash map to store (value → index) as we iterate.
 *   - For each element check if (target - element) already exists in the map.
 *
 * Complexity:
 *   Time:  O(n)
 *   Space: O(n)
 */

#include <bits/stdc++.h>
using namespace std;

// ─── Solution ────────────────────────────────────────────────────────────────

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < (int)nums.size(); i++) {
            int complement = target - nums[i];
            if (seen.count(complement))
                return {seen[complement], i};
            seen[nums[i]] = i;
        }
        return {};
    }
};

// ─── Local Testing ────────────────────────────────────────────────────────────

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    Solution sol;
    vector<int> nums = {2, 7, 11, 15};
    auto ans = sol.twoSum(nums, 9);
    cout << "[" << ans[0] << ", " << ans[1] << "]\n"; // [0, 1]

    return 0;
}
