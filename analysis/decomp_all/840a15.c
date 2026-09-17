
uint FUN__text1__00840a15(int *param_1,int param_2)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  uint local_c;
  
  if (((param_1 == (int *)0x0) || (param_1[7] == 0)) || (*param_1 == 0)) {
    return 0xfffffffe;
  }
  uVar3 = (param_2 != 4) - 1 & 0xfffffffb;
  local_c = 0xfffffffb;
  do {
    switch(*(undefined4 *)param_1[7]) {
    case 0:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 4) = (uint)*(byte *)*param_1;
      uVar2 = *(uint *)(param_1[7] + 4);
      *param_1 = *param_1 + 1;
      if ((uVar2 & 0xf) != 8) {
        *(undefined4 *)param_1[7] = 0xd;
        param_1[6] = (int)"unknown compression method";
        *(undefined4 *)(param_1[7] + 4) = 5;
        local_c = uVar3;
        break;
      }
      if (*(uint *)(param_1[7] + 0x10) < (*(uint *)(param_1[7] + 4) >> 4) + 8) {
        *(undefined4 *)param_1[7] = 0xd;
        param_1[6] = (int)"invalid window size";
        *(undefined4 *)(param_1[7] + 4) = 5;
        local_c = uVar3;
        break;
      }
      *(undefined4 *)param_1[7] = 1;
      local_c = uVar3;
    case 1:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      bVar1 = *(byte *)*param_1;
      *param_1 = *param_1 + 1;
      if ((*(int *)(param_1[7] + 4) * 0x100 + (uint)bVar1) % 0x1f == 0) {
        if ((bVar1 & 0x20) != 0) {
          *(undefined4 *)param_1[7] = 2;
          local_c = uVar3;
          goto switchD__text1__00840a78_caseD_2;
        }
        *(undefined4 *)param_1[7] = 7;
        local_c = uVar3;
      }
      else {
        *(undefined4 *)param_1[7] = 0xd;
        param_1[6] = (int)"incorrect header check";
        *(undefined4 *)(param_1[7] + 4) = 5;
        local_c = uVar3;
      }
      break;
    case 2:
switchD__text1__00840a78_caseD_2:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = (uint)*(byte *)*param_1 << 0x18;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 3;
      local_c = uVar3;
switchD__text1__00840a78_caseD_3:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1 * 0x10000;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 4;
      local_c = uVar3;
switchD__text1__00840a78_caseD_4:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1 * 0x100;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 5;
      local_c = uVar3;
switchD__text1__00840a78_caseD_5:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1;
      *param_1 = *param_1 + 1;
      param_1[0xc] = *(int *)(param_1[7] + 8);
      *(undefined4 *)param_1[7] = 6;
      return 2;
    case 3:
      goto switchD__text1__00840a78_caseD_3;
    case 4:
      goto switchD__text1__00840a78_caseD_4;
    case 5:
      goto switchD__text1__00840a78_caseD_5;
    case 6:
      *(undefined4 *)param_1[7] = 0xd;
      param_1[6] = (int)"need dictionary";
      *(undefined4 *)(param_1[7] + 4) = 0;
      return 0xfffffffe;
    case 7:
      local_c = FUN__text1__00844daf(*(undefined4 *)(param_1[7] + 0x14),param_1,local_c);
      if (local_c == 0xfffffffd) {
        *(undefined4 *)param_1[7] = 0xd;
        *(undefined4 *)(param_1[7] + 4) = 0;
        local_c = 0xfffffffd;
      }
      else {
        if (local_c == 0) {
          local_c = uVar3;
        }
        if (local_c != 1) {
          return local_c;
        }
        FUN__text1__00844c00(*(undefined4 *)(param_1[7] + 0x14),param_1,param_1[7] + 4);
        if (*(int *)(param_1[7] + 0xc) == 0) {
          *(undefined4 *)param_1[7] = 8;
          local_c = uVar3;
          goto switchD__text1__00840a78_caseD_8;
        }
        *(undefined4 *)param_1[7] = 0xc;
        local_c = uVar3;
      }
      break;
    case 8:
switchD__text1__00840a78_caseD_8:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = (uint)*(byte *)*param_1 << 0x18;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 9;
      local_c = uVar3;
switchD__text1__00840a78_caseD_9:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1 * 0x10000;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 10;
      local_c = uVar3;
switchD__text1__00840a78_caseD_a:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1 * 0x100;
      *param_1 = *param_1 + 1;
      *(undefined4 *)param_1[7] = 0xb;
      local_c = uVar3;
switchD__text1__00840a78_caseD_b:
      if (param_1[1] == 0) {
        return local_c;
      }
      param_1[1] = param_1[1] + -1;
      param_1[2] = param_1[2] + 1;
      *(uint *)(param_1[7] + 8) = *(int *)(param_1[7] + 8) + (uint)*(byte *)*param_1;
      *param_1 = *param_1 + 1;
      if (*(int *)(param_1[7] + 4) == *(int *)(param_1[7] + 8)) {
        *(undefined4 *)param_1[7] = 0xc;
LAB__text1__008410aa:
        return 1;
      }
      *(undefined4 *)param_1[7] = 0xd;
      param_1[6] = (int)"incorrect data check";
      *(undefined4 *)(param_1[7] + 4) = 5;
      local_c = uVar3;
      break;
    case 9:
      goto switchD__text1__00840a78_caseD_9;
    case 10:
      goto switchD__text1__00840a78_caseD_a;
    case 0xb:
      goto switchD__text1__00840a78_caseD_b;
    case 0xc:
      goto LAB__text1__008410aa;
    case 0xd:
      return 0xfffffffd;
    default:
      return 0xfffffffe;
    }
  } while( true );
}

