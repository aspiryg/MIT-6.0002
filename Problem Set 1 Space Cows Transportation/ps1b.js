function dpWakeWeight(eggWeights, targetWeight, memo = {}) {
  let result = [0, 0, []];
  if (eggWeights.length === 0 || targetWeight <= 0) {
    return result;
  }
  if (memo[(eggWeights, targetWeight)]) {
    return memo[(eggWeights, targetWeight)];
  }

  let branchResult = [0, 0, []];
  let leastBranch = 0;
  for (let i = 0; i < eggWeights.length; ++i) {
    let egg = eggWeights[i];
    if (eggWeights[i] > targetWeight) {
      // Do somthing
      let newEggWeights = eggWeights.filter((_, eg) => eg !== i);
      branchResult = dpWakeWeight(newEggWeights, targetWeight, memo);
    } else {
      // Do other
      branchResult = [1, egg, [egg]];
      let recResult = dpWakeWeight(eggWeights, targetWeight - egg, memo);
      branchResult[0] = branchResult[0] + recResult[0];
      branchResult[1] = branchResult[1] + recResult[1];
      branchResult[2] = [...branchResult[2], ...recResult[2]];
    }
    if (branchResult[0] < leastBranch || leastBranch === 0) {
      leastBranch = branchResult[0];
      result = branchResult;
      memo[(eggWeights, targetWeight)] = result;
    }
  }
  return result;
}

let first = ["A", "B", "D", "C"];
let third = ["R", "P"];
// let second = first.filter((_, i) => i !== 0);
// console.log(second);
// let commbine = [...first, ...third];
// console.log(commbine);

// let mybject = {};
// mybject[first] = 5;
// mybject[third] = 6;

// console.log(mybject[third]);

let myList = [1, 5, 10, 25, 8, 9, 12, 60];
let n = 928;

let result = dpWakeWeight(myList, n, {});

console.log(result);
