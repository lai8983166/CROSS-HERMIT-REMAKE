
void FUN__text__0047a590(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_24 = (int)*local_10;
  switch(local_24) {
  case 0:
    FUN__text__0046b0f0(param_1,1);
    FUN__text__0046b0b0(param_1,1);
    *local_10 = *local_10 + '\x01';
    break;
  case 1:
    local_18 = FUN__text__0046aa40(CONCAT31(*local_10 >> 7,
                                            *(undefined1 *)(*(int *)(param_1 + 600) + 0xa4)));
    local_1c = FUN__text__0046aa40(*(undefined1 *)(param_1 + 0x500));
    local_14 = (int)(char)(&DAT_00618d40)[local_1c + local_18 * 5];
    if (local_14 == -1) {
      *local_10 = *local_10 + '\x01';
    }
    else {
      FUN__text__0046bcc0(param_1,local_14);
      *local_10 = *local_10 + '\x01';
    }
    *(undefined2 *)(param_1 + 10) = 0;
    break;
  case 2:
    iVar1 = FUN__text__00469eb0(param_1);
    if (iVar1 == 0) {
      iVar1 = FUN__text__00469f90(param_1);
      if (iVar1 == 0) {
        iVar1 = FUN__text__00469d30(param_1);
        if (iVar1 == 0) {
          iVar1 = FUN__text__00469df0(param_1);
          if (iVar1 == 0) {
            local_20 = 0x3c;
          }
          else {
            local_20 = 0x3e;
          }
        }
        else {
          local_20 = 0x3e;
        }
      }
      else {
        local_20 = 0x25;
      }
    }
    else {
      local_20 = 0x48;
    }
    if (local_20 <= *(short *)(param_1 + 10)) {
      *local_10 = *local_10 + '\x01';
    }
    break;
  case 3:
    *(undefined1 *)(*(int *)(param_1 + 600) + 0xa4) = *(undefined1 *)(param_1 + 0x500);
    iVar1 = FUN__text__00468d80(param_1);
    if (iVar1 == 0) {
      *(undefined2 *)(param_1 + 0x4fe) = 600;
    }
    else {
      *(undefined2 *)(param_1 + 0x4fe) = 900;
    }
    FUN__text__0046c290(param_1);
    FUN__text__0046b0b0(param_1,0);
    FUN__text__0046b0f0(param_1,0);
    iVar1 = FUN__text__00469c60(param_1);
    if (iVar1 == 0) {
      FUN__text__00475270(param_1,2);
    }
    else {
      FUN__text__00475270(param_1,0x1c);
    }
    iVar1 = FUN__text__00468d80(param_1);
    if (iVar1 == 0) {
      *(undefined1 *)(*(int *)(param_1 + 600) + 0x9f) = 2;
    }
  }
  local_8 = 0x47a7de;
  FUN__text__0056ce80();
  return;
}

