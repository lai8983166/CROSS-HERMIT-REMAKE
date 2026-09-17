
bool FUN__text1__0084c931(int *param_1)

{
  int iVar1;
  int iVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  undefined2 uVar5;
  
  if (DAT_00872874 != 0) {
    iVar2 = param_1[5];
    if ((iVar2 != DAT_00872908) || (iVar2 != DAT_00872918)) {
      if (DAT_008757e8 == 0) {
        FUN__text1__0084cadd(1,1,iVar2,4,1,0,0,2,0,0,0);
        FUN__text1__0084cadd(0,1,param_1[5],10,5,0,0,2,0,0,0);
      }
      else {
        if (DAT_00875888 != 0) {
          uVar4 = 0;
          uVar3 = 0;
          uVar5 = DAT_0087588e;
        }
        else {
          uVar4 = DAT_0087588c;
          uVar3 = DAT_0087588e;
          uVar5 = 0;
        }
        FUN__text1__0084cadd
                  (1,DAT_00875888 == 0,iVar2,DAT_0087588a,uVar3,uVar4,uVar5,DAT_00875890,
                   DAT_00875892,DAT_00875894,DAT_00875896);
        if (DAT_00875834 != 0) {
          uVar4 = 0;
          uVar3 = 0;
          iVar2 = param_1[5];
          uVar5 = DAT_0087583a;
        }
        else {
          iVar2 = param_1[5];
          uVar4 = DAT_00875838;
          uVar3 = DAT_0087583a;
          uVar5 = 0;
        }
        FUN__text1__0084cadd
                  (0,DAT_00875834 == 0,iVar2,DAT_00875836,uVar3,uVar4,uVar5,DAT_0087583c,
                   DAT_0087583e,DAT_00875840,DAT_00875842);
      }
    }
    iVar2 = param_1[7];
    if (DAT_0087290c < DAT_0087291c) {
      if ((DAT_0087290c <= iVar2) && (iVar2 <= DAT_0087291c)) {
        if ((DAT_0087290c < iVar2) && (iVar2 < DAT_0087291c)) {
          return true;
        }
LAB__text1__0084caa9:
        iVar1 = ((param_1[2] * 0x3c + param_1[1]) * 0x3c + *param_1) * 1000;
        if (iVar2 == DAT_0087290c) {
          return DAT_00872910 <= iVar1;
        }
        return iVar1 < DAT_00872920;
      }
    }
    else {
      if (iVar2 < DAT_0087291c) {
        return true;
      }
      if (DAT_0087290c < iVar2) {
        return true;
      }
      if ((iVar2 <= DAT_0087291c) || (DAT_0087290c <= iVar2)) goto LAB__text1__0084caa9;
    }
  }
  return false;
}

