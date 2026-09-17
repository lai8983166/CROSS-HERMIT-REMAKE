
void FUN__text__0043e010(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((DAT_007a49fc != 0) &&
     (local_c = (int *)FUN__text__004142b0(), *(short *)(DAT_007a49fc + 0xb288) == 0)) {
    (**(code **)(*local_c + 0xfc))(local_c,0,4,4);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,5,2);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,6,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,1,4);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,2,2);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0xfc))(local_c,0,3,0);
    FUN__text__0056ce80();
    local_18 = *(undefined4 *)(local_8 + 0x110);
    switch(local_18) {
    case 0:
      (**(code **)(*local_c + 0xfc))(local_c,0,0x12,0);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x10,0);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x11,0);
      FUN__text__0056ce80();
      break;
    case 1:
      (**(code **)(*local_c + 0xfc))(local_c,0,0x12,1);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x10,1);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x11,1);
      FUN__text__0056ce80();
      break;
    case 2:
      (**(code **)(*local_c + 0xfc))(local_c,0,0x12,2);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x10,2);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x11,2);
      FUN__text__0056ce80();
      break;
    case 3:
      (**(code **)(*local_c + 0xfc))(local_c,0,0x12,3);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x10,3);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 0xfc))(local_c,0,0x11,3);
      FUN__text__0056ce80();
    }
    (**(code **)(*local_c + 200))(local_c,0x1b,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0xf,1);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x18,0);
    FUN__text__0056ce80();
    (**(code **)(*local_c + 200))(local_c,0x19,5);
    FUN__text__0056ce80();
    local_1c = *(int *)(local_8 + 0x10c);
    if (local_1c == 1) {
      (**(code **)(*local_c + 200))(local_c,0xe,0);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x13,5);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x14,6);
      FUN__text__0056ce80();
    }
    else if (local_1c == 2) {
      (**(code **)(*local_c + 200))(local_c,0xe,0);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x13,5);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x14,7);
      FUN__text__0056ce80();
    }
    else {
      (**(code **)(*local_c + 200))(local_c,0xe,1);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x13,2);
      FUN__text__0056ce80();
      (**(code **)(*local_c + 200))(local_c,0x14,1);
      FUN__text__0056ce80();
    }
    (**(code **)(*local_c + 0xf4))(local_c,0,*(undefined4 *)(local_8 + 0xdc));
    FUN__text__0056ce80();
    (**(code **)(*local_c + 0x130))(local_c,0x1c4);
    FUN__text__0056ce80();
    for (local_14 = 0; local_14 != 0x25; local_14 = local_14 + 1) {
      for (local_10 = 0; local_10 != 0x21; local_10 = local_10 + 1) {
        if ((*(uint *)(local_8 + local_14 * 0x1080 + 0x140 + local_10 * 0x80) & 0xff000000) != 0) {
          (**(code **)(*local_c + 0x120))
                    (local_c,6,2,local_8 + 0x130 + local_14 * 0x1080 + local_10 * 0x80,0x20);
          FUN__text__0056ce80();
        }
      }
    }
  }
  local_8 = 0x43e523;
  FUN__text__0056ce80();
  return;
}

