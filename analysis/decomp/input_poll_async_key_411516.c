
void input_poll_async_key(void)

{
  int unaff_EBP;
  undefined *puStack0000006c;
  
  while (*(int *)(unaff_EBP + -0x10) != 0x100) {
    if (*(char *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x380) ==
        *(char *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x480)) {
      *(int *)(unaff_EBP + -0x14) = *(int *)(unaff_EBP + -0x14) + 1;
    }
    if (*(char *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x480) != '\0') {
      *(int *)(unaff_EBP + -0x18) = *(int *)(unaff_EBP + -0x18) + 1;
    }
    *(int *)(unaff_EBP + -0x10) = *(int *)(unaff_EBP + -0x10) + 1;
  }
  if ((*(int *)(unaff_EBP + -0x14) == 0x100) && (*(int *)(unaff_EBP + -0x18) != 0)) {
    if (*(int *)(*(int *)(unaff_EBP + -4) + 0x88c) == 0) {
      if (*(int *)(*(int *)(unaff_EBP + -4) + 0x880) <= *(int *)(*(int *)(unaff_EBP + -4) + 0x888))
      {
        *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x88c) = 1;
        *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x888) = 0;
        *(undefined4 *)(unaff_EBP + -0x10) = 0;
        while (*(int *)(unaff_EBP + -0x10) != 0x100) {
          *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x680) =
               *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x680) |
               *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x480);
          *(int *)(unaff_EBP + -0x10) = *(int *)(unaff_EBP + -0x10) + 1;
        }
      }
    }
    else if (*(int *)(*(int *)(unaff_EBP + -4) + 0x884) <=
             *(int *)(*(int *)(unaff_EBP + -4) + 0x888)) {
      *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x88c) = 1;
      *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x888) = 0;
      *(undefined4 *)(unaff_EBP + -0x10) = 0;
      while (*(int *)(unaff_EBP + -0x10) != 0x100) {
        *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x680) =
             *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x680) |
             *(byte *)(*(int *)(unaff_EBP + -4) + *(int *)(unaff_EBP + -0x10) + 0x480);
        *(int *)(unaff_EBP + -0x10) = *(int *)(unaff_EBP + -0x10) + 1;
      }
    }
    *(int *)(*(int *)(unaff_EBP + -4) + 0x888) = *(int *)(*(int *)(unaff_EBP + -4) + 0x888) + 1;
  }
  else {
    *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x88c) = 0;
    *(undefined4 *)(*(int *)(unaff_EBP + -4) + 0x888) = 0;
  }
  **(undefined4 **)(unaff_EBP + -8) = *(undefined4 *)(*(int *)(unaff_EBP + -8) + 4);
  *(undefined4 *)(*(int *)(unaff_EBP + -8) + 4) = 0;
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x548) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 1;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x550) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 2;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x54b) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 4;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x54d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 8;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4d2) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x10;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4cf) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x20;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4d0) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x40;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4d1) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x80;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4cb) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x100;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4cc) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x200;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4cd) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x400;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4c7) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x800;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4c8) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x1000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4c9) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x2000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x49c) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x4000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4b9) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x8000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x481) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x10000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4aa) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x20000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x4b6) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x20000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x49d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x40000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x51d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 4) = *(uint *)(*(int *)(unaff_EBP + -8) + 4) | 0x40000;
  }
  *(uint *)(*(int *)(unaff_EBP + -8) + 8) =
       (**(uint **)(unaff_EBP + -8) ^ *(uint *)(*(int *)(unaff_EBP + -8) + 4)) &
       *(uint *)(*(int *)(unaff_EBP + -8) + 4);
  *(uint *)(*(int *)(unaff_EBP + -8) + 0x10) =
       (**(uint **)(unaff_EBP + -8) ^ *(uint *)(*(int *)(unaff_EBP + -8) + 4)) &
       **(uint **)(unaff_EBP + -8);
  *(undefined4 *)(*(int *)(unaff_EBP + -8) + 0xc) = 0;
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x748) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 1;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x750) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 2;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x74b) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 4;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x74d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 8;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6d2) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x10;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6cf) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x20;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6d0) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x40;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6d1) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x80;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6cb) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x100;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6cc) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x200;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6cd) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x400;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6c7) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x800;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6c8) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x1000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6c9) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x2000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x69c) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x4000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6b9) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x8000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x681) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x10000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6aa) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x20000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x6b6) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x20000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x69d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x40000;
  }
  if ((*(byte *)(*(int *)(unaff_EBP + -4) + 0x71d) & 0x80) != 0) {
    *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) = *(uint *)(*(int *)(unaff_EBP + -8) + 0xc) | 0x40000;
  }
  puStack0000006c = &UNK_00411cef;
  __chkesp();
  return;
}

