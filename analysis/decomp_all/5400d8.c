
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__005400d8(int param_1,float param_2)

{
  uint uVar1;
  float fVar2;
  int iVar3;
  char *pcVar4;
  undefined1 local_34 [4];
  undefined1 local_30 [4];
  undefined1 local_2c [4];
  undefined1 local_28 [4];
  undefined4 local_24;
  uint local_20;
  uint local_1c;
  float local_18;
  undefined4 local_14;
  uint local_10;
  uint local_c;
  float local_8;
  
  switch(param_2) {
  case 5.60519e-45:
    FUN__text__00548e8a(&local_10);
    FUN__text__00548e8a(&param_2);
    if ((((uint)param_2 | local_10) & 0xffffff00) == 0) {
      *(undefined4 *)(param_1 + 0xac) = 0;
      uVar1 = (uint)param_2 | 0xfffffe00;
LAB__text__00540147:
      *(uint *)(param_1 + 0xb4) = uVar1 << 8 | local_10;
      goto switchD__text__005400f9_caseD_1f;
    }
    goto LAB__text__00540129;
  case 7.00649e-45:
    FUN__text__00548e8a(&local_10);
    FUN__text__00548e8a(&param_2);
    if ((((uint)param_2 | local_10) & 0xffffff00) == 0) {
      *(undefined4 *)(param_1 + 0xac) = 1;
      uVar1 = (uint)param_2 | 0xffffff00;
      goto LAB__text__00540147;
    }
LAB__text__00540129:
    pcVar4 = "invalid version";
LAB__text__0054012e:
    FUN__text__0053eb92(param_1,pcVar4);
  case 8.40779e-45:
  case 9.80909e-45:
  case 1.12104e-44:
  case 1.26117e-44:
  case 1.54143e-44:
  case 1.68156e-44:
  case 6.30584e-44:
  case 6.44597e-44:
    goto switchD__text__005400f9_caseD_6;
  case 1.4013e-44:
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(local_28);
    FUN__text__00548e8a(local_2c);
    FUN__text__00548e8a(local_30);
    FUN__text__00548e8a(local_34);
    FUN__text__0053f8ca(param_2,local_34);
    goto switchD__text__005400f9_caseD_6;
  case 1.82169e-44:
    FUN__text__00548e8a(&local_1c);
    FUN__text__00548e8a(&local_c);
    FUN__text__00548e1c(local_c);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 4;
    goto switchD__text__005400f9_caseD_6;
  case 1.96182e-44:
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(&local_1c);
    FUN__text__00548e8a(&local_c);
    FUN__text__00548e1c(local_c);
    FUN__text__00548e1c(local_1c | (uint)param_2);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 8;
    goto switchD__text__005400f9_caseD_6;
  case 2.10195e-44:
    FUN__text__00548e8a(&local_10);
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(&local_1c);
    FUN__text__00548e8a(&local_c);
    FUN__text__00548e1c(local_c);
    FUN__text__00548e1c(local_1c | (uint)param_2);
    FUN__text__00548e1c(local_10);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 0xc;
    goto switchD__text__005400f9_caseD_6;
  case 2.24208e-44:
    FUN__text__00548e8a(&local_20);
    FUN__text__00548e8a(&local_10);
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(&local_1c);
    FUN__text__00548e8a(&local_c);
    if ((*(int *)(param_1 + 0xac) == 0) && ((local_c & 0xffff) == 3)) {
      local_c = local_c & 0xffff0002 | 2;
      local_20 = local_20 ^ 0x1000000;
    }
    FUN__text__00548e1c(local_c);
    FUN__text__00548e1c(local_1c | (uint)param_2);
    FUN__text__00548e1c(local_10);
    FUN__text__00548e1c(local_20);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 0x10;
    goto switchD__text__005400f9_caseD_6;
  case 2.38221e-44:
    FUN__text__00548e8a(&local_24);
    FUN__text__00548e8a(&local_20);
    FUN__text__00548e8a(&local_10);
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(&local_1c);
    FUN__text__00548e8a(&local_c);
    FUN__text__00548e1c(local_c);
    FUN__text__00548e1c(local_1c | (uint)param_2);
    FUN__text__00548e1c(local_10);
    FUN__text__00548e1c(local_20);
    FUN__text__00548e1c(local_24);
    *(int *)(param_1 + 0xa0) = *(int *)(param_1 + 0xa0) + 0x14;
    goto switchD__text__005400f9_caseD_6;
  case 2.52234e-44:
    FUN__text__00548e8a(&param_2);
    param_2 = (float)((uint)param_2 | 0xf0000);
    fVar2 = param_2;
    break;
  case 2.66247e-44:
    FUN__text__00548fbd(&local_14);
    FUN__text__00548e8a(param_1 + 0x3e4);
    *(undefined4 *)(param_1 + 0x3e0) = 1;
    FUN__text__00548e8a(&param_2);
    uVar1 = FUN__text__0053f3df(local_14);
    fVar2 = (float)(uVar1 | (uint)param_2 & 0xfff0ffff);
    param_2 = fVar2;
    goto LAB__text__0054045d;
  case 2.8026e-44:
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e1c(param_2);
    if (((*(int *)(param_1 + 0xb4) != -0xfefc) || (((uint)param_2 & 0x70000000) != 0x20000000)) ||
       (((uint)param_2 & 0xf000000) == 0)) goto switchD__text__005400f9_caseD_6;
    pcVar4 = "constant modifiers not supported in ps.1.4";
    goto LAB__text__0054012e;
  case 2.94273e-44:
    FUN__text__00548e8a(&param_2);
    if ((*(int *)(param_1 + 0xb4) == -0xfefc) && (((uint)param_2 & 0x70000000) == 0x20000000)) {
      pcVar4 = "constant modifiers not supported in ps.1.4";
LAB__text__005404f9:
      FUN__text__0053eb92(param_1,pcVar4);
      fVar2 = param_2;
    }
    else {
      uVar1 = (uint)param_2 & 0xf000000;
      if (uVar1 == 0) {
        param_2 = (float)((uint)param_2 & 0xf1ffffff | 0x1000000);
        fVar2 = param_2;
      }
      else if (uVar1 == 0x2000000) {
        param_2 = (float)((uint)param_2 & 0xf3ffffff | 0x3000000);
        fVar2 = param_2;
      }
      else if (uVar1 == 0x4000000) {
        param_2 = (float)((uint)param_2 & 0xf5ffffff | 0x5000000);
        fVar2 = param_2;
      }
      else if (uVar1 == 0x7000000) {
        param_2 = (float)((uint)param_2 & 0xf8ffffff | 0x8000000);
        fVar2 = param_2;
      }
      else if ((uVar1 == 0x9000000) || (fVar2 = param_2, uVar1 == 0xa000000)) {
        pcVar4 = "negate and divide modifiers cannot be combined";
        goto LAB__text__005404f9;
      }
    }
    break;
  case 3.08286e-44:
    FUN__text__00548e8a(&local_8);
    FUN__text__00548e8a(&param_2);
    if (*(int *)(param_1 + 0xac) == 0) {
      pcVar4 = "complement not supported in vertex shaders";
LAB__text__005405d2:
      FUN__text__0053eb92(param_1,pcVar4);
    }
    else {
      if ((*(int *)(param_1 + 0xb4) == -0xfefc) && (((uint)param_2 & 0x70000000) == 0x20000000)) {
        pcVar4 = "constant modifiers not supported in ps.1.4";
        goto LAB__text__005405d2;
      }
      if (((uint)param_2 & 0xf000000) != 0) {
        pcVar4 = "complement cannot be used with other modifiers";
        goto LAB__text__005405d2;
      }
    }
    param_2 = (float)((uint)param_2 & 0xf6ffffff | 0x6000000);
    fVar2 = param_2;
    break;
  case 3.22299e-44:
    FUN__text__00548e8a(&param_2);
    fVar2 = (float)((uint)param_2 & 0xffe4ffff | 0xe40000);
    break;
  case 3.36312e-44:
    FUN__text__00548fbd(&local_14);
    FUN__text__00548e8a(param_1 + 0x3e4);
    *(undefined4 *)(param_1 + 0x3e0) = 1;
    FUN__text__00548e8a(&param_2);
    uVar1 = FUN__text__0053f488(local_14);
    fVar2 = (float)(uVar1 | (uint)param_2 & 0xff00ffff);
    goto LAB__text__0054045d;
  case 3.50325e-44:
    FUN__text__00548fbd(&local_14);
    FUN__text__00548e8a(param_1 + 0x3e4);
    *(undefined4 *)(param_1 + 0x3e0) = 1;
    uVar1 = FUN__text__0053f529(local_14,0,0);
    FUN__text__00548e1c(uVar1 | 0x80000000);
    FUN__text__00428ad0(local_14);
    *(undefined4 *)(param_1 + 0x3e0) = 0;
    goto switchD__text__005400f9_caseD_6;
  case 3.64338e-44:
    FUN__text__00548fbd(&local_14);
    FUN__text__00548e8a(param_1 + 0x3e4);
    *(undefined4 *)(param_1 + 0x3e0) = 1;
    FUN__text__00548e8a(&local_8);
    uVar1 = FUN__text__0053f529(local_14,local_8,1);
    fVar2 = (float)(uVar1 | 0x80000000);
LAB__text__0054045d:
    FUN__text__00548e1c(fVar2);
    FUN__text__00428ad0(local_14);
    *(undefined4 *)(param_1 + 0x3e0) = 0;
    goto switchD__text__005400f9_caseD_6;
  case 3.78351e-44:
    FUN__text__00548e8a(&local_8);
    if (*(int *)(param_1 + 0xac) == 0) {
      if (local_8 != -4.656613e-10) {
        pcVar4 = "illegal register in index expression";
        goto LAB__text__00540722;
      }
    }
    else {
      pcVar4 = "syntax error";
LAB__text__00540722:
      FUN__text__0053eb92(param_1,pcVar4);
    }
    fVar2 = 1.14794e-41;
    break;
  case 3.92364e-44:
    FUN__text__00548e8a(&local_8);
    fVar2 = local_8;
    if (((uint)local_8 & 0xffffe000) != 0) {
      FUN__text__0053eb92(param_1,"illegal register number");
      fVar2 = local_8;
    }
    break;
  case 4.06377e-44:
    FUN__text__00548e8a(&param_2);
    FUN__text__00548e8a(&local_8);
    if (*(int *)(param_1 + 0xac) == 0) {
      if (local_8 != -4.656613e-10) {
        pcVar4 = "illegal register in index expression";
        goto LAB__text__005407ab;
      }
      if (((uint)param_2 & 0x2000) != 0) {
        pcVar4 = "a0.x can only appear once in an index expression";
        goto LAB__text__005407ab;
      }
    }
    else {
      pcVar4 = "syntax error";
LAB__text__005407ab:
      FUN__text__0053eb92(param_1,pcVar4);
    }
    fVar2 = (float)((uint)param_2 | 0x2000);
    break;
  case 4.2039e-44:
    FUN__text__00548e8a(&local_8);
    FUN__text__00548e8a(&param_2);
    if ((((uint)param_2 & 0x1fff) + (int)local_8 & 0xffffe000) != 0) {
      FUN__text__0053eb92(param_1,"illegal register number");
    }
    fVar2 = (float)(((int)local_8 + (int)param_2 ^ (uint)param_2) & 0x1fff ^ (uint)param_2);
    break;
  case 4.34403e-44:
switchD__text__005400f9_caseD_1f:
    *(undefined4 *)(param_1 + 0x3dc) = *(undefined4 *)(param_1 + 0x1d0);
    goto switchD__text__005400f9_caseD_6;
  case 4.48416e-44:
  case 4.76441e-44:
  case 5.04467e-44:
  case 5.32493e-44:
  case 5.60519e-44:
    uVar1 = *(uint *)(param_1 + 0x1c8);
    goto LAB__text__00540812;
  case 4.62428e-44:
  case 4.90454e-44:
  case 5.1848e-44:
  case 5.46506e-44:
  case 5.74532e-44:
    if (*(int *)(param_1 + 0xac) == 0) {
      FUN__text__0053eb92(param_1,"coissue not supported in vertex shaders");
    }
    uVar1 = *(uint *)(param_1 + 0x1c8) | 0x40000000;
LAB__text__00540812:
    FUN__text__00548e1c(uVar1);
    FUN__text__00548e1c(*(undefined4 *)(param_1 + 0x1cc));
    FUN__text__0053fa49();
    goto switchD__text__005400f9_caseD_6;
  case 5.88545e-44:
  case 6.02558e-44:
    FUN__text__00548e8a(&local_8);
    fVar2 = (float)(int)local_8;
    local_18 = fVar2;
    if ((int)local_8 < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
      local_18 = fVar2;
    }
    break;
  case 6.16571e-44:
    FUN__text__00548e8a(&local_8);
    fVar2 = (float)(int)local_8;
    if ((int)local_8 < 0) {
      fVar2 = fVar2 + _DAT_005d0a44;
    }
    fVar2 = -fVar2;
    local_18 = fVar2;
    break;
  case 6.5861e-44:
    FUN__text__00548e8a(&local_18);
    fVar2 = -local_18;
    local_18 = -local_18;
    break;
  case 6.72623e-44:
    FUN__text__00548f0a(param_1 + 200);
    fVar2 = *(float *)(param_1 + 0x1d0);
    break;
  case 6.86636e-44:
    fVar2 = (float)FUN__text__00572840(param_1 + 200);
    break;
  case 7.00649e-44:
    FUN__text__00572990(param_1 + 200,&DAT_005d15e8,&local_18);
    fVar2 = local_18;
    break;
  default:
    goto switchD__text__005400f9_default;
  }
  FUN__text__00548e1c(fVar2);
switchD__text__005400f9_caseD_6:
switchD__text__005400f9_default:
  iVar3 = FUN__text__00548ff1();
  if (((iVar3 < 0) || (iVar3 = FUN__text__00548ebe(), iVar3 < 0)) ||
     ((iVar3 = FUN__text__00548ebe(), iVar3 < 0 ||
      (((iVar3 = FUN__text__00548ebe(), iVar3 < 0 || (iVar3 = FUN__text__00548ebe(), iVar3 < 0)) ||
       (iVar3 = FUN__text__00548ebe(), iVar3 < 0)))))) {
    FUN__text__0053eb92(param_1,"Internal assembler error! %d",0x3bb);
  }
  return;
}

